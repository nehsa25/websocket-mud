import boto3
import os
from botocore.exceptions import NoCredentialsError
from dontcheckin import Secrets

AWS_REGION = Secrets.AWS_REGION
BUCKET_NAME = Secrets.BUCKET_NAME

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)


class AWSUtility:
    @staticmethod
    def generate_public_url(file_name):
        return f"{Secrets.S3Url}{file_name}"

    @staticmethod
    def upload_image_to_s3(
        image_path, s3_key, make_public=True, content_type="image/svg+xml"
    ):
        try:
            extra_args = {}
            if make_public:
                extra_args["ACL"] = "public-read"
            extra_args["ContentType"] = content_type
            s3_client.upload_file(image_path, BUCKET_NAME, s3_key, ExtraArgs=extra_args)
        except FileNotFoundError:
            raise f"Error: File not found at {image_path}"
        except NoCredentialsError:
            raise "Error: AWS credentials not found. Configure your AWS credentials."
