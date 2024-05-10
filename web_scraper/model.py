from typing import Any

from pydantic import BaseModel


class Joker(BaseModel):

    num: int
    name: str
    link: str
    image: str
    rarity: str
    cost: str

    def header_fields(self) -> list[str]:
        curr_fields = self.model_fields
        curr_fields.pop("link", None)
        header_fields = list(curr_fields.keys())
        header_fields.append("gold sticker")
        return header_fields
