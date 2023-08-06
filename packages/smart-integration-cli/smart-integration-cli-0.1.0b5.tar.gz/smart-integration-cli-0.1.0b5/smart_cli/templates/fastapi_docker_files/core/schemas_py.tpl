from typing import Optional, Any, Union, List, Optional
from pydantic import BaseModel


class BasePaginationSchema(BaseModel):
    count: int
    next: Optional[str]
    prev: Optional[str]
    results: Any


class DefaultResponseSchema(BaseModel):
    success: bool = True
    message: str


class SelectionSchema(BaseModel):
    code: Union[str, int]
    value: str
    enums: List[Optional['SelectionSchema']]


class FilterSchema(BaseModel):
    code: Union[str, int]
    name: str
