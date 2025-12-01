from pydantic import BaseModel
from typing import List, Optional

class InvoiceLine(BaseModel):
    line_id: int
    item_id: str
    description: Optional[str]
    quantity: float
    unit_price: float
    currency: str

class InvoiceHeader(BaseModel):
    invoice_id: str
    vendor_id: str
    vendor_name: Optional[str]
    currency: str
    total_amount: float
    lines: List[InvoiceLine]
