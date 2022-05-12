from ast import parse
import os
from flask import Flask, render_template, request, flash, redirect, url_for
from unicodedata import name
from forms import ImageForm
from werkzeug.utils import secure_filename
from PIL import Image, ImageFilter
from PIL.ExifTags import TAGS
import requests
from io import BytesIO
# from dotenv import load_dotenv
from models import db, connect_db, ImageData, Photos
# load_dotenv()
import boto3
import uuid
from botocore.exceptions import ClientError


#/upload get form with image, save form, save data to db, done

#/edit - download image(again),



app = Flask(__name__)

### S3 Keys
app.config['ACCESS_KEY'] = os.environ['ACCESS_KEY']
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

### DB Configs
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = (
        os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))


connect_db(app)
db.create_all()

# @app.route('/', methods=["GET"])
# def displayHome():
#     return render_template("landing.html")

"""Display Image from url from bucket"""
@app.route('/images/<filename>', methods=["GET"])
def displayImages(filename):

    #downloads image url :)
    image_url = f'https://s3.us-west-1.amazonaws.com/pix.ly/{filename}'
    img = Image.open(requests.get(image_url, stream=True).raw)
    img.save(f'./static/downloads/WALRUS.jpeg')


    # image_blur = image.filter(ImageFilter.BLUR)
    # image_blur.save(f'./static/downloads/blur-{filename}')
    #do image manipulation here

    return render_template("images.html", url=image_url)


@app.route('/images/add', methods=["GET","POST"])
def addImage():

 # dataflow: client -img-> form -img-> server -img-> s3, server -data-> db

    #take file from client/browser
    #send image to s3
    #send metadata to metadata table
    #send image name & url to images table
    #slugify filenames
    form = ImageForm()

    if form.validate_on_submit():
        print("FORM VALIDATED")
        #sends to bucket

        size = 1200, 1200
        filename = secure_filename(form.image.data.filename)
        file_name = uuid.uuid1()

        form.image.data.save(f'./static/downloads/{filename}')
        image = Image.open(f'./static/downloads/{filename}')
        image.thumbnail(size)
        ext = image.format.lower()

        image.save(f'./static/downloads/{file_name}.{ext}')

        send_to_bucket(f'./static/downloads/{file_name}', file_name)

        image_url = f'https://s3.us-west-1.amazonaws.com/pix.ly/{file_name}'

        #posts to databse
        photo = Photos(image_key=f'{file_name}.{ext}', image_url=image_url)
        db.session.add(photo)


        parseMetadata( image, filename)

        db.session.commit()

        return redirect(f'/images/')

    return render_template("imageForm.html", form=form)


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
    aws_access_key_id=app.config['ACCESS_KEY'],
    aws_secret_access_key=app.config['SECRET_KEY']
)

@app.route('/images/<image>', methods=["POST"])
def editImage(image):


    return render_template("editingPage.html")




"""upload image to s3 bucket, return url"""
def send_to_bucket(path, name, bucket="pix.ly"):
    try:
        print("uploading file...")
        client_s3.upload_file(path, bucket, name)

        #client_s3.upload_fileobj(image.read(), bucket_name, "TESTINGG!!!")

    except ClientError as err:
        print("CLIENTERROR: ",err)

    except Exception as err:
        print("EXCEPTION: ",err)


"""Extracts exif data from image object"""
def parseMetadata(image, image_key):
    exif_data = image.getexif()
    if exif_data:
# iterating over all EXIF data fields
        for tag_id in exif_data:
            # get the tag name, instead of human unreadable tag id
            tag = TAGS.get(tag_id, tag_id)
            data = exif_data.get(tag_id)
            # decode bytes
            if isinstance(data, bytes):
                data = data.decode()
                image_data =ImageData(image_key=image_key, image_type=tag,image_value=data)
                db.session.add(image_data)
                print(f"{tag:25}: {data}")
            image_data =ImageData(image_key=image_key, image_type=tag,image_value=str(data))
            db.session.add(image_data)
            print(image_data)
            #Raw exif looks like: {296: 2, 34665: 90, 274: 1, 282: 144.0, 283: 144.0, 40962: 1357, 40963: 1277, 37510: b'ASCII\x00\x00\x00Screenshot'}
            #TODO: come back to it if we have more time for GPS