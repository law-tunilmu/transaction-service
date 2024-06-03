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

class CreditCardConfig(BaseModel):
    secure: bool
    channel: str
    bank: str
    installment: Optional[dict] = None
    whitelist_bins: Optional[List[str]] = None
    dynamic_descriptor: Optional[dict] = None

class PaymentOption(BaseModel):
    pass

class BCAKlikVA(PaymentOption):
    va_number: str
    sub_company_code: str
    free_text: Optional[dict] = None

class BNIVA(PaymentOption):
    va_number: str

class BRIVA(PaymentOption):
    va_number: str

class CIMBVA(PaymentOption):
    va_number: str

class PermataVA(PaymentOption):
    va_number: str
    recipient_name: str

class Gopay(PaymentOption):
    enable_callback: bool
    callback_url: str

class Expiry(BaseModel):
    start_time: str
    unit: str
    duration: int

class PageExpiry(BaseModel):
    duration: int
    unit: str

class TransactionDetails(BaseModel):
    order_id: str
    gross_amount: int


class SnapTransaction(BaseModel):
    transaction_details: TransactionDetails
    item_details: Optional[List[Item]] = None
    customer_details: CustomerDetails
    enabled_payments: List[str]
    credit_card: Optional[CreditCardConfig] = None
    bca_va: Optional[BCAKlikVA] = None
    bni_va: Optional[BNIVA] = None
    bri_va: Optional[BRIVA] = None
    cimb_va: Optional[CIMBVA] = None
    permata_va: Optional[PermataVA] = None
    gopay: Optional[Gopay] = None
    expiry: Optional[Expiry] = None
    page_expiry: Optional[PageExpiry] = None


class User(BaseModel):
    email = str