from joblib import Parallel
from tqdm import tqdm

from db import S3Connector, Serializer, Deserializer

s3 = S3Connector()
serializer = Serializer()
deserializer = Deserializer(schema_id=2)

def raw_to_clean():
    for obj in s3.get_list_object("raw"):
        raw = deserializer(obj)
        raw_content = raw["after"]