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


# """Display Image from url from bucket"""
# @app.route('/images/<filename>', methods=["GET"])
# def displayImages(filename):

#     #downloads image url :)
#     image_url = f'https://s3.us-west-1.amazonaws.com/pix.ly/{filename}'
#     img = Image.open(requests.get(image_url, stream=True).raw)
#     img.save(f'./static/downloads/WALRUS.jpeg')


#     # image_blur = image.filter(ImageFilter.BLUR)
#     # image_blur.save(f'./static/downloads/blur-{filename}')
#     #do image manipulation here

#     return render_template("images.html", url=image_url)


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

        filename = secure_filename(form.image.data.filename)
        #Standardizes filenames
        file_name = str(uuid.uuid1())
        image_url = f'https://s3.us-west-1.amazonaws.com/pix.ly/{file_name}'

        form.image.data.save(f'./static/downloads/{filename}')
        image = Image.open(f'./static/downloads/{filename}')

        # Sets max resolution
        size = 1200, 1200
        image.thumbnail(size)

        ext = image.format.lower()
        image.save(f'./static/downloads/{file_name}.{ext}')

        send_to_bucket(f'./static/downloads/{file_name}.{ext}', file_name)

        #posts to databse
        photo = Photos(image_key=f'{file_name}', image_url=image_url)
        db.session.add(photo)


        parseMetadata(image, file_name)
        db.session.commit()

        if os.path.exists(f'./static/downloads/{file_name}.{ext}'):
            os.remove(f'./static/downloads/{file_name}.{ext}')

        return redirect(f'/images/{file_name}')

    return render_template("imageForm.html", form=form)


@app.route('/images/<image>', methods=["GET", "POST"])
def editImage(image):

    photo = Photos.query.get_or_404(image)


    return render_template("editingPage.html",photo=photo)



""" Connect to S3 Service """

client_s3 = boto3.client(
    's3',
    'us-west-1',
    aws_access_key_id=app.config['ACCESS_KEY'],
    aws_secret_access_key=app.config['SECRET_KEY']
)


#TODO: move thesde back to helper file

def send_to_bucket(path, name, bucket="pix.ly"):
    """upload image to s3 bucket
    args( file path, file name, default bucket)
    """
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