from typing import Dict, Iterable

from confluent_kafka import Consumer, KafkaError, OFFSET_BEGINNING, TopicPartition
from confluent_kafka.admin import AdminClient

from bytewax.inputs import FixedPartitionedSource, StatefulSourcePartition



class KafkaInput(FixedPartitionedSource):
    def __init__(
        self,
        brokers: Iterable[str],
        topics: Iterable[str],
        starting_offset: int = OFFSET_BEGINNING,
    ):
        self._brokers = brokers
        self._topics = topics
        self._starting_offset = starting_offset

        if isinstance(brokers, str):
            raise TypeError("brokers must be an iterable and not a string")


    def list_parts(self):
        config = {
            "bootstrap.servers": ",".join(self._brokers),
        }
        client = AdminClient(config)

        return list(set(self._list_parts(client, self._topics)))
    
    def _list_parts(self, client, topics):
        for topic in topics:
            # List topics one-by-one so if auto-create is turned on,
            # we respect that.
            cluster_metadata = client.list_topics(topic)
            topic_metadata = cluster_metadata.topics[topic]
            if topic_metadata.error is not None:
                raise RuntimeError(
                    f"error listing partitions for Kafka topic `{topic!r}`: "
                    f"{topic_metadata.error.str()}"
                )
            part_idxs = topic_metadata.partitions.keys()
            for i in part_idxs:
                yield f"{i}-{topic}"


    def build_part(self, step_id, for_part, resume_state):
        part_idx, topic = for_part.split("-", 1)
        part_idx = int(part_idx)
        assert topic in self._topics, "Can't resume from different set of Kafka topics"

        config = {
            # We'll manage our own "consumer group" via recovery
            # system.
            'bootstrap.servers': ",".join(self._brokers),
            'group.id': "default",
            'auto.offset.reset': "earliest"
        }
        consumer = Consumer(config)
        return _KafkaSource(
            consumer, topic, part_idx, self._starting_offset, resume_state
        )
    

class _KafkaSource(StatefulSourcePartition):
    def __init__(self, consumer, topic, part_idx, starting_offset, resume_state):
        self._offset = resume_state or starting_offset
        # Assign does not activate consumer grouping.
        consumer.assign([TopicPartition(topic, part_idx, self._offset)])
        self._consumer = consumer
        self._topic = topic


    def next_batch(self):
        msg = self._consumer.poll(1.0)  # seconds
        if msg is None:
            return []
        elif msg.error() is not None:
            if msg.error().code() == KafkaError._PARTITION_EOF:
                raise StopIteration()
            else:
                raise RuntimeError(
                    f"error consuming from Kafka topic `{self.topic!r}`: {msg.error()}"
                )
        else:
            item = (msg.key(), msg.value())
            # Resume reading from the next message, not this one.
            self._offset = msg.offset() + 1
            return [item]

    def close(self):
        self._consumer.close()

    def snapshot(self):
        return self._offset