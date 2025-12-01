from app.agents.planner import deterministic_plan
from app.agents.executor import execute_plan
from app.agents.auditor import audit_decision

def test_end_to_end_perfect_match():
    plan = deterministic_plan("INV-5001","PO-1001")
    result = execute_plan(plan)
    decision = audit_decision(result)
    assert decision["decision"] == "APPROVE"

def test_end_to_end_mismatch():
    plan = deterministic_plan("INV-5002","PO-1002")
    result = execute_plan(plan)
    decision = audit_decision(result)
    assert decision["decision"] == "ESCALATE"
    assert "price_mismatch" in decision["reasons"]
