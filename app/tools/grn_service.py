from fastapi import APIRouter
from typing import Dict
router = APIRouter()

# Lightweight mock: pretend we have GRN recorded quantities for PO
GRN_DATA = {
    "PO-1001": {"received_qty": {1:10, 2:5}},
    "PO-1002": {"received_qty": {1:10, 2:5}}
}

@router.get("/get_grn_status/{po_id}", tags=["erp"])
def get_grn_status(po_id: str):
    data = GRN_DATA.get(po_id, {"received_qty": {}})
    return {"po_id": po_id, "grn_summary": data}
