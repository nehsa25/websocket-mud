import inspect
import boto3
import os
from botocore.exceptions import NoCredentialsError

from log_utils import LogUtils
from settings.exception import ExceptionUtils

AWS_REGION = 'us-west-2'
BUCKET_NAME = 'nehsa-storage'

# Option 1: Configure credentials using environment variables
s3_client = boto3.client('s3', region_name=AWS_REGION,
                       aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                       aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

# Option 2: Configure credentials directly (not recommended for production)
# s3_client = boto3.client('s3', region_name=AWS_REGION,
#                        aws_access_key_id='YOUR_ACCESS_KEY_ID',
#                        aws_secret_access_key='YOUR_SECRET_ACCESS_KEY')

# Option 3: Rely on IAM role (recommended for EC2 instances)
# s3_client = boto3.client('s3', region_name=AWS_REGION)

class S3Utils:
    @staticmethod
    def upload_image_to_s3(image_path, s3_key, make_public=True, content_type = 'image/svg+xml', logger=None):
        try:
            method_name = inspect.currentframe().f_code.co_name
            LogUtils.debug(f"{method_name}: enter", logger)

            extra_args = {}
            if make_public:
                extra_args['ACL'] = 'public-read'
            
            extra_args['ContentType'] = content_type

            s3_client.upload_file(image_path, BUCKET_NAME, s3_key, ExtraArgs=extra_args)

            public_url = f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"
            LogUtils.info(f"{method_name}: exit, public_url: {public_url}", logger)
            return public_url

        except FileNotFoundError:
            LogUtils.error(f"Error: File not found at {image_path}")
            return None    
        except NoCredentialsError:
            LogUtils.error("Error: AWS credentials not found. Configure your AWS credentials.")
            return None    
        except Exception as e:
            LogUtils.error(f"Error: {ExceptionUtils.print_exception(e)}", logger)
            return None