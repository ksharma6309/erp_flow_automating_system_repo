from app.agents.planner import deterministic_plan

def test_plan_structure():
    plan = deterministic_plan("INV-5001","PO-1001")
    assert "steps" in plan
    assert "required_tool_calls" in plan
    assert plan["deterministic"] is True
    assert plan["validation_rules"]["line_quantity_tolerance"] == 0.0