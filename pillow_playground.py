from PIL import Image , ExifTags




img = Image.open('files/6f4435c4dc8346d7b9da7c9382c46bb1.jpeg')
img_exif = img._getexif()
#{296: 2, 34665: 90, 274: 1, 282: 144.0, 283: 144.0, 40962: 1357, 40963: 1277, 37510: b'ASCII\x00\x00\x00Screenshot'}


#TODO: come back to it if we have more time for GPS
if img_exif:
    for key, val in img_exif.items():
        if key in ExifTags.TAGS:
            print("THIS IS THE PIL EXIF",f'{ExifTags.TAGS[key]}:{val}')
breakpoint()