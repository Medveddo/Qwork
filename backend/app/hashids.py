import os
from typing import Optional

from hashids import Hashids


class LocalHashIds:
    HASHIDS_SALT = os.getenv("HASHIDS_SALT", "dev-omega-salt")
    HASHIDS_MIN_LENGTH = 16

    def __init__(self) -> None:
        self.hashids = Hashids(salt=self.HASHIDS_SALT, min_length=self.HASHIDS_MIN_LENGTH)

    def to_hash_id(self, id_: int) -> str:
        return self.hashids.encode(id_)

    def from_hash_id(self, hashid: str) -> Optional[int]:
        ids = self.hashids.decode(hashid)
        if not ids:
            return None

        return ids[0]


hashids_ = LocalHashIds()
