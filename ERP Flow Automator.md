🧠 ERP Flow Automator - Capstone Project – Google Kaggle: Enterprise AI Systems

This project implements an enterprise-grade Agentic ERP Automation System that automates:

Invoice ↔ Purchase Order (PO) Matching

Inventory Availability Checking

GRN (Goods Receipt) Status Lookup

Deterministic Audit Validation

The system uses the Planner → Executor → Auditor agent pipeline, OpenAPI-defined ERP tools, FastAPI backend, Streamlit UI, SQLite mock ERP database, and full append-only HMAC-signed audit logs.

🏗 1. Project Architecture
1.1 High-Level Overview
User → Streamlit UI → Planner Agent → Executor Agent → Auditor Agent → Decision

Components:

Planner Agent
Generates deterministic plan (JSON) → No tool calls

Executor Agent
Calls ERP mock tools strictly per OpenAPI schema

Auditor Agent
Applies versioned audit rules → APPROVE or ESCALATE

SQLite Mock ERP
PO, Invoice, GRN, Inventory

Streamlit UI
Run visualization, mismatch tables, logs, inventory lookup

Audit Layer
HMAC-signed logs, append-only, exportable

🗂 2. Repository Structure
/app
  /agents
    planner.py
    executor.py
    auditor.py

  /tools
    po_service.py
    invoice_service.py
    inventory_service.py
    grn_service.py

  /schemas
    po_models.py
    invoice_models.py

  /rules
    matching_rules.json
    audit_policies.json

  /audit
    log_manager.py

  /db
    init_db.py
    seed_data.sql
    erp.db

  main.py

/ui
  streamlit_app.py

/tests
  test_planner.py
  test_executor.py
  test_auditor.py

Dockerfile
docker-compose.yml
requirements.txt
README.md

📐 3. Architecture Diagram
                   +-----------------------+
                   |     Streamlit UI      |
                   | (Input, Trace, Audit) |
                   +-----------+-----------+
                               |
                               v
                     +---------+---------+
                     |    Planner Agent   |
                     |  (Deterministic)   |
                     +---------+---------+
                               |
                               v
                      +--------+---------+
                      |   Executor Agent  |
                      |  (OpenAPI Tools)  |
                      +----+----+----+---+
                           |    |    |
  -------------------------+    |    +-------------------------
  |                             |                               |
  v                             v                               v
/get_purchase_order      /get_invoice                    /check_inventory
/get_grn_status (bonus)

/(SQLite Mock ERP Database)

🔄 4. Sequence Diagram (Planner → Executor → Auditor)
User
 │
 │ 1. invoice_id, po_id
 ▼
UI
 │
 │→ call /run-agent
 ▼
Planner Agent
 │
 │→ deterministic JSON plan
 ▼
Executor Agent
 │
 │→ call OpenAPI ERP tools:
        get_purchase_order
        get_invoice
        check_inventory
        get_grn_status
 │
 │→ produce tool call trace log
 ▼
Auditor Agent
 │
 │→ apply matching_rules.json
 │→ apply audit_policies.json
 │→ produce APPROVE/ESCALATE
 ▼
UI (Mismatch Table + Final Decision)

⚙️ 5. Backend (FastAPI) – How It Works
Features:

Strict OpenAPI tool schema

SQLite ERP database

Pydantic models

Deterministic planner

Executor rejects tools not in schema

Auditor loads versioned JSON rules

HMAC-signed audit logs

Idempotent invoice processing

Tools:
Tool	Description
/get_purchase_order/{po_id}	Returns PO Header + Line Items
/get_invoice/{invoice_id}	Returns Invoice Header + Lines
/check_inventory/{item_id}	Returns stock availability
/get_grn_status/{po_id}	Bonus: Returns GRN info
🎨 6. Streamlit UI Overview
UI Sections:

Input Panel
Enter invoice_id & po_id.

Planner Output Viewer
Displays JSON of planner steps.

Executor Call Trace
Shows each tool call: request → response.

Auditor Decision Panel
Shows APPROVE or ESCALATE + Reasons.

Mismatch Summary Table

| Field | PO Value | Invoice Value | Status |


Audit Log Viewer
Scrollable + Download CSV/JSON.

Inventory Lookup Panel
Enter item_id → show stock status.

UI is intentionally clean and enterprise-simple.

🧪 7. Testing
Included Tests:

✔ Planner output structure
✔ Executor blocks non-schema calls
✔ Auditor mismatch detection
✔ End-to-end run
✔ Sample DB seed tests

Run tests:

pytest -q

🔐 8. Security & Non-Functional Requirements
✔ Deterministic behavior (no LLM randomness)
✔ HMAC signed logs
✔ No sensitive data in logs
✔ Handles 100 invoices < 5 seconds
✔ Stateless agents
✔ ERP DB abstracted for future SAP/Oracle/NetSuite connectors
🐳 9. How to Run (Docker or Local)
Option A — Local Setup
1. Install dependencies:
pip install -r requirements.txt

2. Initialize database:
cd app/db
python init_db.py

3. Start FastAPI backend:
cd app
uvicorn main:app --reload --port 8000

4. Run Streamlit UI:
cd ui
streamlit run streamlit_app.py

Option B — Docker Setup
1. Build + Run:
docker-compose up --build


Backend runs on: http://localhost:8000

UI runs on: http://localhost:8501

📤 10. Sample Requests & Responses
10.1 Get PO
GET /get_purchase_order/1001


Response:

{
  "po_id": "1001",
  "vendor": "ACME SUPPLIES",
  "total": 1200,
  "lines": [
    {"item_id": "SKU-1", "qty": 10, "price": 120}
  ]
}

10.2 Get Invoice
GET /get_invoice/INV-9001

✔ 11. Demo Scenario: PERFECT MATCH
Input:
invoice_id = INV-100
po_id = PO-100

Auditor Result:
APPROVE

Mismatch Table:

All green ✔

❌ 12. Demo Scenario: MISMATCH
Input:
invoice_id = INV-102
po_id = PO-100

Auditor Result:
ESCALATE

Reasons:

Quantity mismatch

Total amount mismatch

Mismatch Table Example:
Field	PO	Invoice	Status
Quantity	10	12	❌
Total	1200	1400	❌
🧾 13. Audit Logs

Written via log_manager.py

Append-only

Each entry is HMAC-signed

Exportable in CSV/JSON from UI

🏁 14. Conclusion

This project demonstrates:

Enterprise-grade ERP automation

Deterministic Agentic AI design

Rigorously structured Planner → Executor → Auditor pipeline

Strict OpenAPI tool calling

Full auditability and traceability

Professional UI for ERP workflows