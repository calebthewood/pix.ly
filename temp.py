
import os
from app import send_to_bucket
from flask import Flask, jsonify, render_template, request, flash, redirect, send_file, url_for
from unicodedata import name

from sqlalchemy import null
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
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

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


""" returns sepia Image from url from bucket"""
@app.route('/images/sepia/<filename>', methods=["GET"])
def displayImages(filename):

    #downloads image url :)
    image_url = f'https://s3.us-west-1.amazonaws.com/pix.ly/{filename}'
    img = Image.open(requests.get(image_url, stream=True).raw)

    sepia_name = f'sepia-{str(uuid.uuid1())}.{img.format}'
    sepia_path = f'./static/downloads/{sepia_name}'
    sepia = sepia_filter(img)

    sepia.save(sepia_path)

    #returns pillow img. filter from stack overflow
    send_to_bucket(sepia_path, sepia_name)

    sepia_url = f'https://s3.us-west-1.amazonaws.com/pix.ly/{sepia_name}'


    # image_blur = image.filter(ImageFilter.BLUR)
    # image_blur.save(f'./static/downloads/blur-{filename}')
    #do image manipulation here
    return jsonify({ sepia_url })

################ Filters

def sepia_filter(img):
    width, height = img.size

    pixels = img.load() # create the pixel map

    for py in range(height):
        for px in range(width):
            r, g, b = img.getpixel((px, py))

            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            if tr > 255:
                tr = 255

            if tg > 255:
                tg = 255

            if tb > 255:
                tb = 255

            pixels[px, py] = (tr,tg,tb)

    return img