from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Follows(db.Model):
    """Connection of a follower <-> followed_user."""

    __tablename__ = 'photos'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    image_key = db.Column(
        db.Text,
        nullable=False,
    )

    #optional TODO: to make it more complicated, we can do metadata_1, metadata_2
    height = db.Column(
        db.Text,
        nullable=False,
    )
    #TODO: FIND OUT IF TIMESTAMP IS THE SAME FORMATTING FOR EXIF
    width = db.Column(
        db.Text,
        nullable=False,
    )



def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)




