from .configuration import Configuration
import boto3
config = Configuration()

__all__ = ["config"]

s3 = boto3.client('s3',
                  endpoint_url=f"https://{config.s3_params['S3_ENDPOINT']}",
                  aws_access_key_id=config.s3_params['S3_ACCESS_KEY'],
                  aws_secret_access_key=config.s3_params['S3_SECRET_KEY'])