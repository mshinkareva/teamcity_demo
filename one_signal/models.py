from typing import Optional, Union

from pydantic.dataclasses import dataclass

@dataclass
class FlingPush:
    book_id: str
    title: str
    text: str
    user_ids: list[str]
    picture: str

@dataclass
class Subscription:
    id: str
    identifier: str
    device_os: Optional[str]= None
    device_type: Optional[int] = None
    device_model: Optional[str] = None
    tags: Optional[str] = None
    created_at: Optional[str] = None
    invalid_identifier: Optional[bool] = None
    external_user_id: str | int | None = None

    def __hash__(self) -> int:
        return hash(self.external_user_id)

    def __eq__(self, other):
        return self.external_user_id == other.external_user_id

@dataclass
class Identity:
    external_id: str
    onesignal_id: str

@dataclass
class OneSignalUser:
    subscriptions: Optional[list[Subscription]] = None
    identity: Optional[Identity] = None




