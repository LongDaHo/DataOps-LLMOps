from utils import logger_utils
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from typing import Union

from configs import settings


logger = logger_utils.get_logger(__name__)

class S3Connector:
    _instance: Union[boto3.client, None] = None
    # _deserializer: Union[AvroDeserializer, None] = None

    def __init__(self) -> None:
        if self._instance is None:
            try:
                self._instance = boto3.client('s3',
                    endpoint_url=settings.MINIO_ENDPOINT,
                    aws_access_key_id=settings.MINIO_ACCESS_KEY,
                    aws_secret_access_key=settings.MINIO_SECRET_KEY)
            except ClientError as e:
                logger.error(e)
        
    def get_list_object(self, bucket_name):
        try:
            results = []
            objects_list = self._instance.list_objects_v2(Bucket=bucket_name).get("Contents")
            for obj in objects_list:
                obj_name = obj["Key"]
                response = self._instance.get_object(Bucket=bucket_name, Key=obj_name)
                object_content = response["Body"].read()
                results.append(object_content)
            return results
        except Exception:
            logger.error("An error occurred while reading data.")


    def write_data(self, bucket, points, deserializer):
        try:
            for point in points:
                # Deserialize message 's key
                key = deserializer(point[0])
                filename = str(datetime.now()) + "." + key["id"].replace('\"', '') + ".avro"
                self._instance.put_object(
                    Bucket=bucket,
                    Key=filename,  # Use message key as file name
                    Body=point[1], # Message 's content
                    ContentType='application/octet-stream')
                logger.info(f"Write file %s to minio!", filename)
        except Exception:
            logger.error("An error occurred while inserting data.")


    def get_bucket(self, bucket):
        self._instance.head_bucket(Bucket=bucket)


    def create_bucket(self, bucket):
        self._instance.create_bucket(Bucket=bucket)

    def close(self):
        if self._instance:
            self._instance.close()
            logger.info("Connected to Minio has been closed.")