
import os
import boto3
from botocore.exceptions import ClientError


access_key = 'AKIARKJWSR3S3LJVR2L7'
secret_key = '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'
bucket_name = 'pix.ly'

file_folder="files"
downloads="downloads"
svg_file = "files/1f418.svg"
jpeg_file = "/Users/calebwood/Desktop/Rithm/week10/exercises/pixly/files/237-536x354.jpeg"
png_file = "files/Screen Shot 2022-04-03 at 9.12.06 AM.png"

""" Connect to S3 Service """

client_s3 = boto3.client(
    's3',
    'us-west-1',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

# try:
#     print("uploading file...")
#     client_s3.upload_file(png_file, bucket_name, "png_pic")

# except ClientError as err:
#     print("CLIENTERROR: ",err)

# except Exception as err:
#     print("ECEPTION: ",err)


"""Downloading File"""

# client_s3.download_file(bucket_name, , "downloads/test.png" )



# import os
# import boto3

# #initiate s3 resource
s3 = boto3.resource('s3')

# # select bucket
my_bucket = s3.Bucket(bucket_name)
# breakpoint()
# print("Bucket Contents: ", my_bucket)
# print("s3: ", s3)

"""download file into current directory"""

for s3_object in my_bucket.objects.all():
    # Need to split s3_object.key into path and file name, else it will give error file not found.
    path, filename = os.path.split(s3_object.key)
    breakpoint()
    print("path: ", path)
    print("file: name: ", filename)
    print("s3_object.key: ", s3_object.key)
    # my_bucket.download_file(s3_object.key, filename)
