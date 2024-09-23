from joblib import Parallel, delayed
from tqdm import tqdm
import json

from db import S3Connector, Serializer, Deserializer
from data_logic.dispatcher import RawDispatcher, CleaningDispatcher, ChunkingDispatcher, EmbeddingDispatcher 

s3 = S3Connector()
serializer = Serializer(schema_id=2)
deserializer = Deserializer(schema_id=2)

def batch_process(obj):
    raw = deserializer(obj)
    raw = json.loads(raw["after"])
    raw["type"] = "articles"
    raw["entry_id"] = raw["_id"]
    raw = RawDispatcher.handle_mq_message(raw)
    clean = CleaningDispatcher.dispatch_cleaner(raw)
    chunks = ChunkingDispatcher.dispatch_chunker(clean)
    for chunk in chunks:
        embed = EmbeddingDispatcher.dispatch_embedder(chunk)

obj_list = s3.get_list_object("raw")
Parallel(n_jobs=8, backend="threading")  \
        (delayed(batch_process)(obj)     \
        for obj in tqdm(obj_list))