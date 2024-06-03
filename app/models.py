from typing import Optional, List

from pydantic import BaseModel

class Item(BaseModel):
    id: str
    price: int
    quantity: int
    name: str

class CustomerDetails(BaseModel):
    first_name: str
    email: str

class TransactionDetails(BaseModel):
    gross_amount: int


class SnapTransaction(BaseModel):
    transaction_details: TransactionDetails
    item_details: Optional[List[Item]] = None
    customer_details: CustomerDetails


class User(BaseModel):
    email: str


class UserCart(BaseModel):
    email: str
    course_id: str