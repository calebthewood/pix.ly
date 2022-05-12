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



@app.route('/images/<filename>', methods=["GET"])
def displayImages(filename):

    image_url = f'https://s3.us-west-1.amazonaws.com/pix.ly/{filename}'

    return render_template("images.html", url=image_url)


@app.route('/images/add', methods=["GET","POST"])
def addImage():

 # dataflow: client -img-> form -img->
 #              server -img-> s3 -url-> server -data-> db

    #take file from client/browser
    #send image to s3
    #send metadata to metadata table
    #send image name & url to images table

    form = ImageForm()

    if form.validate_on_submit():
        print("FORM VALIDATED")

        filename = secure_filename(form.image.data.filename)
        form.image.data.save('downloads/' + filename)

        #do image manipulation here

        send_to_bucket(f'downloads/{filename}', filename)


        # all image urls will be:
        image_url = f'https://s3.us-west-1.amazonaws.com/pix.ly/{filename}'

        #oh, my, god. We don't need to store the whole url,
        #just the file name! url is always the same!

        #redirect to images/image_id - need to strip file type off end.
        return redirect(f'/images/add')


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

# @app.route('/images/<image>', methods=["POST"])
# def editImage(image):
#     return render_template("editingPage.html")




"""upload image to s3 bucket, return url"""
def send_to_bucket(image="", name="", bucket="pix.ly"):
    try:
        print("uploading file...")
        client_s3.upload_file(image, bucket, name)

        #client_s3.upload_fileobj(image.read(), bucket_name, "TESTINGG!!!")

    except ClientError as err:
        print("CLIENTERROR: ",err)

    except Exception as err:
        print("EXCEPTION: ",err)


"""Extracts exif data from image object"""
def parseMetadata(image):
    img_exif = image._getexif()
    if img_exif:
        for key, val in img_exif.items():
            if key in ExifTags.TAGS:
                print("THIS IS THE PIL EXIF",f'{ExifTags.TAGS[key]}:{val}')
    #Raw exif looks like: {296: 2, 34665: 90, 274: 1, 282: 144.0, 283: 144.0, 40962: 1357, 40963: 1277, 37510: b'ASCII\x00\x00\x00Screenshot'}
    #TODO: come back to it if we have more time for GPS