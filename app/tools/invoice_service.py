from fastapi import APIRouter, HTTPException
from pathlib import Path
import sqlite3
from ..schemas.invoice_models import InvoiceHeader
router = APIRouter()
DB_PATH = Path(__file__).parent.parent / "db" / "erp.db"

def query_invoice(invoice_id: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    h = cur.execute("SELECT invoice_id,vendor_id,vendor_name,currency,total_amount FROM invoices WHERE invoice_id=?", (invoice_id,)).fetchone()
    if not h:
        return None
    invoice_id,vendor_id,vendor_name,currency,total_amount = h
    lines = []
    for r in cur.execute("SELECT line_id,item_id,description,quantity,unit_price,currency FROM invoice_lines WHERE invoice_id=? ORDER BY line_id",(invoice_id,)):
        line_id,item_id,description,quantity,unit_price,currency = r
        lines.append({
            "line_id": line_id,
            "item_id": item_id,
            "description": description,
            "quantity": quantity,
            "unit_price": unit_price,
            "currency": currency
        })
    conn.close()
    return {
        "invoice_id": invoice_id,
        "vendor_id": vendor_id,
        "vendor_name": vendor_name,
        "currency": currency,
        "total_amount": total_amount,
        "lines": lines
    }

@router.get("/get_invoice/{invoice_id}", response_model=InvoiceHeader, tags=["erp"])
def get_invoice(invoice_id: str):
    inv = query_invoice(invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return inv
