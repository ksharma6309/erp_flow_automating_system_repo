<img width="1280" height="720" alt="1" src="https://github.com/user-attachments/assets/fb3de572-9b74-4c9e-a33d-52e8f6d97e4e" />


<h1>🧠 ERP Flow Automator - Capstone Project – Google Kaggle: Enterprise AI Systems</h1>


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

<img width="2752" height="1536" alt="ERP Flow Agentic Architecture" src="https://github.com/user-attachments/assets/b42ba988-2688-456c-9928-d21ad4cfbf8f" />


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

<img width="7753" height="5866" alt="ERP Flow Automator Sequence Diagram" src="https://github.com/user-attachments/assets/465f1b31-da5b-42b5-8e75-6d936190face" />


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

Logging	JSON Audit Logs

**📁 Project Structure**

- **ERPFlowAutomator/**
  - **app/**
    - **agents/**
      - `planner.py` — Planner agent implementation
      - `executor.py` — Executor agent & tool caller
      - `auditor.py` — Audit rules & decisioning
    - **tools/**
      - `po_service.py` — mock PO tool (FastAPI)
      - `invoice_service.py`
      - `inventory_service.py`
      - `grn_service.py`
    - **db/**
      - `init_db.py` — schema & seed loader
      - `seed_data.sql`
    - **rules/**
      - `matching_rules.json`
      - `audit_policies.json`
    - `main.py`
  - **ui/**
    - `streamlit_app.py`
    - **audit/**
      - `settings.json`
      - `inventory.json`
  - **tests/**
  - `requirements.txt`
  - `docker-compose.yml`
  - `Dockerfile`
  - `README.md`


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

<img width="1917" height="1014" alt="image" src="https://github.com/user-attachments/assets/0e662f93-f936-4931-a2ad-ae4895fff137" />

<img width="1883" height="1017" alt="image" src="https://github.com/user-attachments/assets/ce18d2f4-0a74-4f08-a48c-d7c7f5eccb03" />

<img width="1884" height="1005" alt="image" src="https://github.com/user-attachments/assets/ce58038d-c429-40fa-9e24-054810636866" />

<img width="1869" height="1019" alt="image" src="https://github.com/user-attachments/assets/08e88ae0-a3bd-4863-8d3c-d19833b36b05" />

<img width="1763" height="1008" alt="image" src="https://github.com/user-attachments/assets/0f141148-c60c-461b-ab0b-f062f0d2178e" />

<img width="1761" height="1018" alt="image" src="https://github.com/user-attachments/assets/5cf90f9f-0d2c-4c89-82f2-99436ededad4" />

<img width="1770" height="987" alt="image" src="https://github.com/user-attachments/assets/d8a011e2-68a8-4d9f-9d28-528f9e376b6d" />

<img width="1876" height="1018" alt="image" src="https://github.com/user-attachments/assets/890a5449-c16d-4649-97d4-3ac3ea9bd2fb" />

<img width="1869" height="987" alt="image" src="https://github.com/user-attachments/assets/08571184-9090-4307-94f2-a89453710702" />



**👩‍💻 Author**

**Khushboo Sharma**

**GitHub:** https://github.com/ksharma6309

**LinkedIn:** https://www.linkedin.com/in/khushboo-sharma-b5b372125/ 

