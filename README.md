<img width="1280" height="720" alt="2" src="https://github.com/user-attachments/assets/f4286c81-9e35-40f8-bd8e-6a4ba682d9dd" />
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

📑** Table of Contents**

1. Introduction

2. Problem Statement

3. Why Agentic AI?

4. Project Overview

5. Architecture

6. Features

7. Modules

8. Tech Stack

9. Project Structure

10. Installation Guide

10. VS Code Commands

11. Running the App

12. API Endpoints

13. Streamlit UI Overview

14. Testing

15. Future Enhancements

16. Screenshots

17. Author

**🧭 Introduction**

ERP Flow Automator is an enterprise-grade agentic AI system designed to automate common ERP finance workflows such as:

Invoice ↔ Purchase Order Matching

GRN Verification

Inventory Stock Audit

Tax Validation

The project is built using the Planner → Executor → Auditor architecture taught in the Google Kaggle 5-Day Agents Bootcamp.

It demonstrates safe tool usage, deterministic execution, traceability, audit logs, and transparent results.

**🧩 Problem Statement**

Manual validation of invoices, POs, GRNs, inventory, and taxes is:

Time-consuming

Error-prone

Highly repetitive

Costly when mismatches slip through

Difficult to audit later

Companies need automated, accurate, transparent ERP validation systems that mimic an auditor’s structured reasoning and apply financial rules safely.

**🤖 Why Agentic AI?**

Traditional AI models “guess” answers.
ERP workflow automation requires:

✔ Deterministic execution
✔ Rule-based auditing
✔ Safe tool call restrictions
✔ Transparent trace logs
✔ Explainable decisions
✔ Error-proof validations

Agentic AI solves this through:

Planner: Generates a structured plan

Executor: Executes only allowed tools

Auditor: Applies rules & produces final decision

This is exactly how enterprise systems must operate.

**🚀 Project Overview**

The ERP Flow Automator includes 4 complete enterprise modules:

1️⃣ PO–Invoice Matching

Matches line items, quantities, unit price, vendor, totals.

2️⃣ GRN Checker

Validates goods received quantity vs PO vs Invoice.

3️⃣ Inventory Stock Checker

Checks if requested items exceed available stock.

4️⃣ Tax Calculator / Validator

Detects incorrect tax values or mismatched tax slabs.

Each module provides:

Full tool-call trace

Human-readable reasoning

Auditor summary

Deterministic decision (APPROVE / ESCALATE)

**🏗️ Architecture**
**Planner → Executor → Auditor flow**

(You can replace with a Mermaid diagram or image)

User Input → Planner Agent → Plan (JSON)
→ Executor Agent → Execution Trace
→ Auditor Agent → Validation Rules → Decision Output

**⭐ Features**

✔ AI-based ERP validation
✔ Deterministic agent plan execution
✔ SQLite mock ERP database
✔ FastAPI backend
✔ Streamlit UI
✔ Full plan + trace + audit logs
✔ Mismatch summary reports
✔ Extendable ERP modules
✔ Docker support

**📦 Modules**
1. PO–Invoice Matching

Compares PO vs Invoice header & line items

Detects qty mismatch, price mismatch, vendor mismatch

Outputs: APPROVE / ESCALATE

2. GRN Checker

Confirms goods received quantity matches PO

Flags partial receipt or excess receipt

3. Inventory Checker

Stock availability check

Ideal for procurement automation

4. Tax Validator

Validates GST/VAT percentages

Recalculates expected tax

**🛠️ Tech Stack**
Layer	Technology
Backend API	FastAPI
Agents	Python (Planner, Executor, Auditor)
UI	Streamlit
Database	SQLite
Tests	PyTest
Packaging	Docker
Logging	JSON Audit Logs

**📁 Project Structure**

ERPFlowAutomator/
│── app/
│   ├── agents/
│   │   ├── planner.py
│   │   ├── executor.py
│   │   └── auditor.py
│   ├── tools/
│   │   ├── invoice_service.py
│   │   ├── po_service.py
│   │   ├── inventory_service.py
│   │   └── grn_service.py
│   ├── db/
│   │   ├── init_db.py
│   │   └── seed_data.sql
│   ├── rules/
│   │   ├── audit_policies.json
│   │   └── matching_rules.json
│   ├── schemas/
│   │   ├── invoice_models.py
│   │   └── po_models.py
│   ├── audit/
│   │   └── audit_log.json
│   └── main.py
│
│── ui/
│   ├── streamlit_app.py
│   └── audit/
│       ├── settings.json
│       └── inventory.json
│
│── tests/
│── requirements.txt
│── docker-compose.yaml
│── Dockerfile
│── README.md

**⚙️ Installation Guide**
1. Create Virtual Environment
python -m venv venv
.\venv\Scripts\activate       # Windows

2. Install Requirements
pip install -r requirements.txt

3. Initialize Database
python app/db/init_db.py

**💻 Terminal Command Prompt Steps**
Open VS Code:
code .

Run FastAPI backend:
uvicorn app.main:app --reload

Run Streamlit UI:
streamlit run ui/streamlit_app.py

🧪 Running Tests
pytest tests/

**🖥️ API Endpoints**
Method	Route	Description
GET	/invoice/{id}	Fetch invoice
GET	/po/{id}	Fetch purchase order
GET	/inventory/{item_id}	Check stock
POST	/validate/po-invoice	Validate invoice vs PO


**🎨 Streamlit UI Overview**

Enter Invoice ID & PO ID

View planner plan

View executor trace

View auditor decision

Download audit log

View mismatch summary chart

**🔮 Future Enhancements**

OCR-based invoice extraction

ML-based anomaly detection

Multi-vendor support

SAP/Oracle ERP connectors

Real audit dashboard

**📸 Screenshots**

(Insert your project images here)

![UI Screenshot](screens/ui.png)
![Planner Screenshot](screens/planner.png)
![Audit Summary](screens/audit.png)

**👩‍💻 Author**

**Khushboo Sharma
GitHub: https://github.com/ksharma6309
LinkedIn: https://www.linkedin.com/in/khushboo-sharma-b5b372125/**
