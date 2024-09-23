import bytewax.operators as op
from bytewax.dataflow import Dataflow

from streaming import KafkaInput
from streaming import MinioOutput

from db import S3Connector
from configs import settings

connection = S3Connector()

flow = Dataflow("Streaming pipeline")
stream = op.input("input", flow, KafkaInput(brokers=[settings.KAFKA_ENDPOINT], topics=[settings.KAFKA_TOPIC]))
op.output("test", stream, MinioOutput(connection=connection))

