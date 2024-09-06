from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    # Minio configs
    MINIO_ENDPOINT: str = "http://localhost:9000"
    MINIO_ACCESS_KEY: str = "minio_access_key"
    MINIO_SECRET_KEY: str = "minio_secret_key"

    # Schema registry configs
    SCHEMA_ENDPOINT: str = "http://localhost:8081"
    SCHEMA_ID_KEY: int = 1
    SCHEMA_ID_VALUE: int = 2

    # Kafka configs
    KAFKA_ENDPOINT: str = "localhost:9092"
    KAFKA_TOPIC: str = "mongo.scrabble.articles"

settings = Setting()