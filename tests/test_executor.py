import os
from app.agents.executor import fetch_openapi, is_tool_allowed

def test_openapi_available():
    # ensure ERP_BASE_URL points to running FastAPI in test environment; this unit test expects server running
    openapi = fetch_openapi()
    assert "paths" in openapi

def test_tool_allowed():
    openapi = fetch_openapi()
    assert is_tool_allowed(openapi, "get_purchase_order")
    assert is_tool_allowed(openapi, "get_invoice")
    assert is_tool_allowed(openapi, "check_inventory")
