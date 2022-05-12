from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Integer


db = SQLAlchemy()

class Photos(db.Model):
    """Store Image key & url"""

    __tablename__ = 'images'

    image_key = db.Column(
        db.Text,
        nullable=False,
        primary_key = True
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    image_data = db.relationship(
        "ImageData",
        backref="images")


    def __repr__(self):
        return f"<Image #{self.id}: {self.image_key}, {self.image_url}>"

    @classmethod
    def add_image(self, key, url):
        """adds image to database"""
        image = Photos(
            image_key=key,
            image_url=url,
        )
        db.session.add(image)
        return image



class ImageData(db.Model):
    """Hold Metadata for images"""

    __tablename__ = 'image_data'

    image_key = db.Column(
        db.Integer,
        db.ForeignKey( "images.image_key", ondelete="cascade"),
        nullable=False,
        primary_key=True
    )

    image_type = db.Column(
        db.Text,
        nullable=False,
        primary_key=True
    )

    image_value = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )








    # #optional TODO: to make it more complicated, we can do metadata_1, metadata_2




def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)




