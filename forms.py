from flask_wtf import FlaskForm
from wtforms import StringField
from flask_wtf.file import FileField


#NOTE: setup form first, add validation later.

class ImageForm(FlaskForm):
    """form for uploading image"""

    image = FileField()
    test = StringField()

    #image = 'FileField(Image File', [regexp('^[^/\\]\.png$')])
    # description  = TextAreaField('Image Description')

    # def validate_image(form, field):
    #     if field.data:
    #         field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)



# def upload(request):
#     form = ImageForm(request.POST)
#     if form.image.data:
#         image_data = request.FILES[form.image.name].read()
#         open(os.path.join(UPLOAD_PATH, form.image.data), 'w').write(image_data)