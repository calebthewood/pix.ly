import boto3
from botocore.exceptions import ClientError
import logging

access_key = 'AKIARKJWSR3S3LJVR2L7'
secret_key = '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'
bucket_name = 'pix.ly'

file_folder="files"
downloads="downloads"
svg_file = "files/1f418.svg"
jpeg_file = "/Users/calebwood/Desktop/Rithm/week10/exercises/pixly/files/237-536x354.jpeg"
png_file = "files/Screen Shot 2022-04-03 at 9.12.06 AM.png"
expiration= 3600
""" Connect to S3 Service """

client_s3 = boto3.client(
    's3',
    'us-west-1',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

# try:
#     print("uploading file...")
#     s3.upload_file(png_file, bucket_name, "png_pic")

# except ClientError as err:
#     print("CLIENTERROR: ",err)

# except Exception as err:
#     print("ECEPTION: ",err)


"""retrieving file url"""


# import os
# import boto3

# #initiate s3 resource


def create_presigned_url(bucket_name, object_name ="1f418.svg", expiration=604800):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = client_s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    print(response)
    return response

create_presigned_url(bucket_name)