from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.schema_registry.avro import AvroDeserializer


from configs import settings

class Serializer:
    def __init__(self, schema_id):
        client = SchemaRegistryClient({"url": settings.SCHEMA_ENDPOINT})
        schema_str = client.get_schema(schema_id=schema_id).schema_str
        self._instance = AvroSerializer(client, schema_str)

    def __call__(self, object_content):
        return self._instance(object_content, None)

class Deserializer:
    def __init__(self, schema_id):
        client = SchemaRegistryClient({"url": settings.SCHEMA_ENDPOINT})
        schema_str = client.get_schema(schema_id=schema_id).schema_str
        self._instance = AvroDeserializer(client, schema_str)

    def __call__(self, object_content):
        return self._instance(object_content, None)