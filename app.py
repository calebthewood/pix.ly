import os
from flask import Flask, render_template, request, flash, redirect, url_for
from unicodedata import name
from forms import ImageForm
from werkzeug.utils import secure_filename
from PIL import Image, ExifTags
from io import BytesIO
# from dotenv import load_dotenv
from models import db, connect_db, ImageData, Photos
# load_dotenv()
import boto3
from botocore.exceptions import ClientError
import logging


access_key = 'AKIARKJWSR3S3LJVR2L7'
secret_key = '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'
bucket_name = 'pix.ly'

file_folder="files"
downloads="downloads"
svg_file = "files/1f418.svg"
jpeg_file = "/Users/calebwood/Desktop/Rithm/week10/exercises/pixly/files/237-536x354.jpeg"
png_file = "files/Screen Shot 2022-04-03 at 9.12.06 AM.png"
expiration= 3600

""" Connect to S3 Service """

client_s3 = boto3.client(
    's3',
    'us-west-1',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)





app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pixly'
app.config['SECRET_KEY'] = "secretkey"
connect_db(app)
db.create_all()

# @app.route('/', methods=["GET"])
# def displayHome():


#     return render_template("landing.html")



# @app.route('/images', methods=["GET"])
# def displayImages():
#       return render_template("images.html")



@app.route('/images/add', methods=["GET","POST"])
def addImage():

    #take file from client/browser
    #send image to s3
    #send metadata to metadata table
    #send image name & url to images table

    form = ImageForm()

    if form.validate_on_submit():
        print("FORM VALIDATED")


        filename = secure_filename(form.image.data.filename)
        form.image.data.save('downloads/' + filename)

        image = Image.open(form.image.data)

        # im = Image.open(BytesIO(form.image.data.read()))
        # im1 = Image.frombytes(image)
        # im2 = BytesIO(form.image.data.read())
        # img = Image.open(form.image.data)

        send_to_bucket(image, filename)


        img_exif = image._getexif()


        
        #{296: 2, 34665: 90, 274: 1, 282: 144.0, 283: 144.0, 40962: 1357, 40963: 1277, 37510: b'ASCII\x00\x00\x00Screenshot'}


        #TODO: come back to it if we have more time for GPS
        if img_exif:
            for key, val in img_exif.items():
                if key in ExifTags.TAGS:
                    print("THIS IS THE PIL EXIF",f'{ExifTags.TAGS[key]}:{val}')
        breakpoint()



        return redirect("/images/add")


    print("FORM NOT VALIDATED")
    return render_template("imageForm.html", form=form)




# @app.route('/images/<image>', methods=["POST"])
# def editImage(image):
#     return render_template("editingPage.html")


def send_to_bucket(image, filename):
    try:
        print("uploading file...")
        client_s3.upload_file(image, bucket_name, filename)

    except ClientError as err:
        print("CLIENTERROR: ",err)

    except Exception as err:
        print("ECEPTION: ",err)
