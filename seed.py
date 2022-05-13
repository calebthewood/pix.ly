from app import db
from models import Photos, ImageData


db.drop_all()
db.create_all()
db.session.commit()