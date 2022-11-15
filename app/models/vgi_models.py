from typing import Optional
from pydantic import BaseModel


class Layer(BaseModel):
    layer_id: int
    name: str
    description: str
    f_table_name: str
    source_description: str
    reference: Optional[list[int]] = None
    keyword: list[int]
    created_at: str
