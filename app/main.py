from fastapi import FastAPI
from .tools import po_service, invoice_service, inventory_service, grn_service
from pathlib import Path

app = FastAPI(title="Mock ERP Tools - OpenAPI", version="1.0.0")

app.include_router(po_service.router)
app.include_router(invoice_service.router)
app.include_router(inventory_service.router)
app.include_router(grn_service.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
