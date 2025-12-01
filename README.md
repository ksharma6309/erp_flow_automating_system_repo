**🧠 ERP Flow Automator - Capstone Project – Google Kaggle: Enterprise AI Systems**

## 📑 Table of Contents
- [Project Summary](#project-summary)
- [Project Description](#project-description)
- [Architecture](#architecture)
- [Features](#features)
- [Modules](#modules)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation Guide](#installation-guide)
- [VS Code Commands](#vs-code-commands)
- [Running the App](#running-the-app)
- [API Endpoints](#api-endpoints)
- [Streamlit UI Overview](#streamlit-ui-overview)
- [Testing](#testing)
- [Future Enhancements](#future-enhancements)
- [Screenshots](#screenshots)
- [Author](#author)


**⭐ PROJECT SUMMARY**

ERP Flow Automator is an intelligent, agentic AI system built using the Planner → Executor → Auditor architecture to automate critical ERP finance workflows. The system validates Purchase Orders (PO), Invoices, GRN receipts, Inventory stock levels, and Tax calculations using safe OpenAPI tools and rule-based audit checks. It delivers deterministic decisions, complete trace logs, mismatch summaries, and human-readable explanations designed for enterprise-grade accuracy and transparency. Built with FastAPI, Python agents, SQLite, and Streamlit UI, this project demonstrates how agentic AI can automate manual ERP validation tasks reliably and reproducibly.

**⭐ PROJECT DESCRIPTION**

Enterprise finance teams spend significant time manually validating invoices, purchase orders, GRN receipts, inventory stock levels, and tax calculations. This process is repetitive, error-prone, difficult to audit, and costly when mismatches slip through. The ERP Flow Automator solves this by applying a structured, deterministic Agentic AI workflow that ensures accuracy, transparency, and safe tool usage according to Google’s Agentic AI Bootcamp standards.

The system follows the Planner → Executor → Auditor pattern.

The Planner Agent generates a structured validation plan that outlines which ERP tools need to be called and in what sequence.

The Executor Agent safely executes only approved OpenAPI-defined tools (such as fetching PO, Invoice, GRN, Inventory, and Tax Rate data). It logs each request–response pair with correlation IDs for full traceability.

The Auditor Agent applies strict business rules (quantity validation, price matching, tax calculation, GRN verification, inventory checks) and produces a final decision — APPROVE or ESCALATE — along with a structured mismatch summary, reason explanation, and audit log entry.

Each module (Invoice ↔ PO Matching, GRN Checker, Inventory Checker, and Tax Validator) is implemented as a fully independent, testable workflow. The Streamlit UI showcases the plan, execution trace, mismatches, and auditor decision with clear, intuitive visualizations. SQLite acts as a lightweight mock ERP backend, enabling rapid testing without external dependencies. The project demonstrates enterprise features like deterministic output, audit-safe logging, extensible rule files, and reproducible workflows — all within a lightweight and developer-friendly architecture.

The outcome is a compact yet powerful demonstration of how agentic AI can automate ERP workflows with accuracy, safety, and full audit compliance, making it ideal for enterprise automation, AI engineering portfolios, and Kaggle capstone evaluation.

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

''' 
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

'''

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
