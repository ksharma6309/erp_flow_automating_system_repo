from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3
from pathlib import Path
from ..schemas.po_models import POHeader, POLine
from typing import List

router = APIRouter()

DB_PATH = Path(__file__).parent.parent / "db" / "erp.db"

def query_po(po_id: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    h = cur.execute("SELECT po_id,vendor_id,vendor_name,currency,total_amount FROM purchase_orders WHERE po_id=?", (po_id,)).fetchone()
    if not h:
        return None
    po_id,vendor_id,vendor_name,currency,total_amount = h
    lines = []
    for r in cur.execute("SELECT line_id,item_id,description,quantity,unit_price,currency FROM po_lines WHERE po_id=? ORDER BY line_id",(po_id,)):
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
        "po_id": po_id,
        "vendor_id": vendor_id,
        "vendor_name": vendor_name,
        "currency": currency,
        "total_amount": total_amount,
        "lines": lines
    }

@router.get("/get_purchase_order/{po_id}", response_model=POHeader, tags=["erp"])
def get_purchase_order(po_id: str):
    po = query_po(po_id)
    if not po:
        raise HTTPException(status_code=404, detail="PO not found")
    return po
