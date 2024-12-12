from pydantic.dataclasses import dataclass

@dataclass
class FlingPush:
    book_id: str
    title: str
    text: str
    user_ids: list[str]
    picture: str