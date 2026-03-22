from pydantic import BaseModel, Field
from typing import List, Optional

class BorrowRecord(BaseModel):
    borrower_name: str = Field(min_length=2)
    borrow_date: str
    return_date: Optional[str] = None

class Book(BaseModel):
    id: int
    title: str = Field(min_length=2)
    author: str
    pages: int = Field(gt=0)
    borrow_records: List[BorrowRecord] = Field(default_factory=list)
