from typing import Optional, Any
from pydantic import BaseModel


class BasePaginationSchema(BaseModel):
    count: int
    next: Optional[str]
    prev: Optional[str]
    results: Any


class DefaultResponseSchema(BaseModel):
    success: bool = True
    message: str
