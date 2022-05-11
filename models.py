from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Integer


db = SQLAlchemy()

class Image(db.Model):
    """Store Image key & url"""

    __tablename__ = 'images'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    image_key = db.Column(
        db.Text,
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    image_data = db.relationship(
        'image_data',
        backref="images")


    def __repr__(self):
        return f"<Image #{self.id}: {self.image_key}, {self.image_url}>"

    @classmethod
    def add_image(key, url):
        """adds image to database"""
        image = Image(
            image_key=key,
            image_url=url,
        )
        db.session.add(image)
        return image



class ImageData(db.Model):
    """Hold Metadata for images"""

    __tablename__ = 'image_data'

    image_id = db.Column(
        db.Integer,
        db.ForeignKey( "images.id", ondelete="cascade"),
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




