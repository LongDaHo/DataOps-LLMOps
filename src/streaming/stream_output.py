from bytewax.outputs import DynamicSink, StatelessSinkPartition

from db import S3Connector, Deserializer
from configs import settings
from utils import logger_utils


logger = logger_utils.get_logger(__name__)

class MinioOutput(DynamicSink):
    def __init__(self, connection: S3Connector):
        self._connection = connection

        try:
            self._connection.get_bucket("raw")
        except Exception as e:
            self._connection.create_bucket("raw")
            logger.info(f"Create bucket raw!")

    def build(self, step_id, worker_index, worker_count) -> StatelessSinkPartition:
        return MinioSink(connection=self._connection, 
                         deserializer=Deserializer(schema_id=settings.SCHEMA_ID_KEY))
    
class MinioSink(StatelessSinkPartition):
    def __init__(self, connection: S3Connector, deserializer: Deserializer):
        self._client = connection
        self._deserializer = deserializer


    def write_batch(self, items) -> None:
        self._client.write_data("warehouse", items, self._deserializer)