import logging
import os
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, LongType, DoubleType, StringType

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("MinIOSparkJob")

conf = SparkConf()

spark = SparkSession.builder.config(conf=conf).getOrCreate()

# Disable below line to see INFO logs
spark.sparkContext.setLogLevel("ERROR")


df = spark.read.parquet("yellow_tripdata_2022-03.parquet")
df.write.saveAsTable("nyctaxi3.trips", format="iceberg")