from typing import Any

from pydantic import BaseModel


class Joker(BaseModel):

    pos: int
    name: str
    image: str
    rarity: str
    cost: str
