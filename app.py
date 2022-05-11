import os
from flask import Flask, render_template, request, flash, redirect, url_for
from unicodedata import name
from forms import ImageForm
from werkzeug.utils import secure_filename

# from dotenv import load_dotenv
from models import db, connect_db, ImageData, Image
# load_dotenv()







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

        return redirect("/images/add")


    print("FORM NOT VALIDATED")
    return render_template("imageForm.html", form=form)




# @app.route('/images/<image>', methods=["POST"])
# def editImage(image):
#     return render_template("editingPage.html")