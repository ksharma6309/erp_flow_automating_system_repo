"""
Planner Agent: deterministic plan generation.
No tool calls allowed. Output is strictly JSON with steps, required tool calls,
validation rules, expected fields.
"""
from typing import Dict, Any
import json
import hashlib

def deterministic_plan(invoice_id: str, po_id: str) -> Dict[str,Any]:
    # deterministic: base plan on sorted input and fixed sequence
    key = f"{invoice_id}:{po_id}"
    seed = int(hashlib.sha256(key.encode()).hexdigest()[:8], 16)
    # fixed step list
    steps = [
        {"id": 1, "name": "fetch_po", "tool": "get_purchase_order", "args": {"po_id": po_id}, "description": "Retrieve PO header and lines"},
        {"id": 2, "name": "fetch_invoice", "tool": "get_invoice", "args": {"invoice_id": invoice_id}, "description": "Retrieve Invoice header and lines"},
        {"id": 3, "name": "line_level_match", "tool": None, "args": {}, "description": "Compare PO and invoice lines for qty/price/item"},
        {"id": 4, "name": "inventory_check", "tool": "check_inventory", "args": {"item_ids": "from_po_lines"}, "description": "Check on-hand inventory for each item"},
        {"id": 5, "name": "audit_decision", "tool": None, "args": {}, "description": "Apply audit rules to produce decision"}
    ]
    # Required tool calls in order (only names and expected response fields)
    required_tool_calls = [
        {"tool_name": "get_purchase_order", "path": "/get_purchase_order/{po_id}", "method":"GET", "expected_response":"POHeader"},
        {"tool_name": "get_invoice", "path": "/get_invoice/{invoice_id}", "method":"GET", "expected_response":"InvoiceHeader"},
        {"tool_name": "check_inventory", "path": "/check_inventory/{item_id}", "method":"GET", "expected_response":"inventory"}
    ]
    validation_rules = {
        "currency_match": True,
        "line_quantity_tolerance": 0.0,
        "price_tolerance_pct": 0.0,
        "allowed_decision_values": ["APPROVE","ESCALATE"]
    }
    expected_fields = {
        "POHeader": ["po_id","vendor_id","currency","total_amount","lines"],
        "InvoiceHeader": ["invoice_id","vendor_id","currency","total_amount","lines"]
    }
    plan = {
        "invoice_id": invoice_id,
        "po_id": po_id,
        "seed": seed,
        "steps": steps,
        "required_tool_calls": required_tool_calls,
        "validation_rules": validation_rules,
        "expected_fields": expected_fields,
        "deterministic": True,
        "version": "1.0"
    }
    return plan

# Simple unit-friendly wrapper
def create_plan_json(invoice_id: str, po_id: str) -> str:
    return json.dumps(deterministic_plan(invoice_id, po_id), indent=2)
