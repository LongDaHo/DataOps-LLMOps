from typing import Optional, Tuple

from models.base import AvroDataModel


class PostChunkModel(AvroDataModel):
    entry_id: str
    platform: str
    chunk_id: str
    chunk_content: str
    author_id: str
    image: Optional[str] = None
    type: str

    def to_payload(self) -> Tuple[str, dict]:
        data = {
            "platform": self.platform,
            "author_id": self.author_id,
            "chunk_id": self.chunk_id,
            "chunk_content": self.chunk_content,
            "image": self.image,
            "type": self.type,
        }

        return self.entry_id, data


class ArticleChunkModel(AvroDataModel):
    entry_id: str
    platform: str
    link: str
    chunk_id: str
    chunk_content: str
    author_id: str
    type: str

    def to_payload(self) -> Tuple[str, dict]:
        data = {
            "platform": self.platform,
            "author_id": self.author_id,
            "chunk_id": self.chunk_id,
            "chunk_content": self.chunk_content,
            "image": self.image,
            "type": self.type,
        }

        return self.entry_id, data


class RepositoryChunkModel(AvroDataModel):
    entry_id: str
    name: str
    link: str
    chunk_id: str
    chunk_content: str
    owner_id: str
    type: str

    def to_payload(self) -> Tuple[str, dict]:
        data = {
            "platform": self.platform,
            "author_id": self.author_id,
            "chunk_id": self.chunk_id,
            "chunk_content": self.chunk_content,
            "image": self.image,
            "type": self.type,
        }

        return self.entry_id, data