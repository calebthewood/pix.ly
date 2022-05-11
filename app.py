import os
# from dotenv import load_dotenv
from models import db, connect_db
from flask import Flask, render_template, request, flash, redirect
# load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pixly'

connect_db(app)


@app.route('/', methods=["GET"])
def displayHome():


    # form = UserAddForm()

    # if form.validate_on_submit():
    #     try:
    #         user = User.signup(
    #             username=form.username.data,
    #             password=form.password.data,
    #             email=form.email.data,
    #             image_url=form.image_url.data or User.image_url.default.arg,
    #         )
    #         db.session.commit()

    #     except IntegrityError:
    #         flash("Username already taken", 'danger')
    #         return render_template('users/signup.html', form=form)


    #     return redirect("/")

    # else:
        # return render_template('users/signup.html', form=form)
    return render_template("landing.html")



@app.route('/images', methods=["GET"])
def displayImages():
      return render_template("images.html")



@app.route('/images/add', methods=["GET","POST"])
def addImage():
      return render_template("imageForm.html")

@app.route('/images/<image>', methods=["POST"])
def editImage(image):
    return render_template("editingPage.html")