import os
from decouple import config
import boto3
from PIL import Image
import PIL.Image
import io

s3 = boto3.resource('s3',aws_access_key_id=config("AWS_ACCESS_KEY_ID"),aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"))

def image_from_s3(bucket, key):
    bucket = s3.Bucket(bucket)
    image = bucket.Object(key)
    if image:
        # img_data = image.get().get('Body').read();
        # return Image.open(io.BytesIO(img_data));
        print(bucket,image)
    else:
        print("No image found with this name")
    return;

# call the function
# image_from_s3("your-aws-bucket-name", "file-path")

# example

image_from_s3("my-hocal-bucket", "shi.jpg")