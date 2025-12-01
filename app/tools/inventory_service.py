from fastapi import APIRouter, HTTPException
from pathlib import Path
import sqlite3
router = APIRouter()
DB_PATH = Path(__file__).parent.parent / "db" / "erp.db"

@router.get("/check_inventory/{item_id}", tags=["erp"])
def check_inventory(item_id: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    r = cur.execute("SELECT on_hand FROM inventory WHERE item_id=?", (item_id,)).fetchone()
    conn.close()
    if r is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "on_hand": r[0]}
