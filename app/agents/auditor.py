"""
Auditor Agent:
- Loads versioned rules from rules/*.json
- Applies deterministic rules and returns APPROVE or ESCALATE with reasons
- Writes audit decisions into audit/log_manager
"""
import json
from pathlib import Path
from typing import Dict, Any, List
from ..audit.log_manager import AuditLogManager

RULES_PATH = Path(__file__).parent.parent / "rules"
LOG_MANAGER = AuditLogManager()

def load_json(fn: Path) -> Dict[str,Any]:
    return json.loads(fn.read_text())

def audit_decision(execution_result: Dict[str,Any]) -> Dict[str,Any]:
    matching = load_json(RULES_PATH / "matching_rules.json")
    policies = load_json(RULES_PATH / "audit_policies.json")
    comparisons = execution_result["comparisons"]
    po = execution_result["po"]
    inv = execution_result["invoice"]

    reasons = []

    # vendor check
    if po["vendor_id"] != inv["vendor_id"]:
        reasons.append("vendor_mismatch")

    # total check (exact)
    if abs(po["total_amount"] - inv["total_amount"]) > matching["rules"]["total_mismatch"].get("tolerance", 0.0):
        reasons.append("total_mismatch")

    # line-level checks
    for comp in comparisons:
        po_line = comp.get("po_line")
        inv_line = comp.get("invoice_line")
        if not po_line or not inv_line:
            reasons.append("missing_po_lines")
            continue
        # quantity
        if abs(po_line["quantity"] - inv_line["quantity"]) > matching["rules"]["quantity_mismatch"].get("tolerance", 0.0):
            reasons.append("quantity_mismatch")
        # price
        if abs(po_line["unit_price"] - inv_line["unit_price"]) > (po_line["unit_price"] * matching["rules"]["price_mismatch"].get("tolerance_pct",0.0)/100.0):
            reasons.append("price_mismatch")

    # dedupe reasons and create final decision
    unique_reasons = sorted(set(reasons))
    decision = "APPROVE" if not unique_reasons else "ESCALATE"
    detail = {
        "decision": decision,
        "reasons": unique_reasons,
        "po_id": po["po_id"],
        "invoice_id": inv["invoice_id"],
        "policy_version": policies.get("version","unknown")
    }
    # Append to signed audit log
    LOG_MANAGER.append_log(detail, extra={"execution_seed": execution_result.get("plan_seed")})
    return detail
