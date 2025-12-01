"""
Executor Agent:
- Accepts the planner output and executes ONLY tool calls defined in the OpenAPI
  of the ERP FastAPI server (app.main).
- Validates requested tool names / paths against the server's openapi.json.
- Logs each tool request/response for full traceability.
"""
import requests
import os
import json
from typing import Dict, Any, List

ERP_BASE = os.getenv("ERP_BASE_URL", "http://localhost:8000")

class ExecutorError(Exception):
    pass

def fetch_openapi():
    url = f"{ERP_BASE}/openapi.json"
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    return r.json()

def is_tool_allowed(openapi: Dict[str,Any], tool_name: str) -> bool:
    # find any operationId or path that contains the tool name
    for path, methods in openapi.get("paths", {}).items():
        for method, meta in methods.items():
            op = meta.get("operationId","")
            # FastAPI operationId is typically something like get_purchase_order_get_purchase_order__po_id__get
            if tool_name in op or tool_name in path:
                return True
    return False

def call_tool(tool_name: str, args: dict) -> Dict[str,Any]:
    # Map known tool names to endpoints.
    # Strict: always validate against openapi.json
    openapi = fetch_openapi()
    if not is_tool_allowed(openapi, tool_name):
        raise ExecutorError(f"Tool {tool_name} is not in OpenAPI schema")
    # call endpoints deterministically
    if tool_name == "get_purchase_order":
        path = f"{ERP_BASE}/get_purchase_order/{args['po_id']}"
        r = requests.get(path, timeout=10)
    elif tool_name == "get_invoice":
        path = f"{ERP_BASE}/get_invoice/{args['invoice_id']}"
        r = requests.get(path, timeout=10)
    elif tool_name == "check_inventory":
        # args may contain 'item_id' single or list
        item_id = args.get("item_id")
        if item_id is None:
            raise ExecutorError("check_inventory requires item_id")
        path = f"{ERP_BASE}/check_inventory/{item_id}"
        r = requests.get(path, timeout=10)
    elif tool_name == "get_grn_status":
        path = f"{ERP_BASE}/get_grn_status/{args['po_id']}"
        r = requests.get(path, timeout=10)
    else:
        raise ExecutorError(f"Unknown/unauthorized tool {tool_name}")

    log_entry = {
        "tool": tool_name,
        "request": {"url": r.request.url, "method": r.request.method},
        "status_code": r.status_code
    }
    try:
        json_resp = r.json()
        log_entry["response"] = json_resp
    except Exception as e:
        log_entry["response"] = {"error": "non-json response", "text": r.text}
    if r.status_code >= 400:
        raise ExecutorError(f"Tool {tool_name} call failed: {r.status_code} {log_entry['response']}")
    return log_entry

def execute_plan(plan: Dict[str,Any]) -> Dict[str,Any]:
    trace = []
    # Step 1: fetch PO
    po_call = call_tool("get_purchase_order", {"po_id": plan["po_id"]})
    trace.append(po_call)
    # Step 2: fetch Invoice
    inv_call = call_tool("get_invoice", {"invoice_id": plan["invoice_id"]})
    trace.append(inv_call)
    # Step 3: line level match is internal: create comparison structure
    po = po_call["response"]
    inv = inv_call["response"]
    comparisons = []
    # create map by item or line_id
    po_map = {(l["line_id"], l["item_id"]): l for l in po["lines"]}
    inv_map = {(l["line_id"], l["item_id"]): l for l in inv["lines"]}
    # union keys
    keys = set(po_map.keys()) | set(inv_map.keys())
    for key in sorted(keys):
        po_line = po_map.get(key)
        inv_line = inv_map.get(key)
        comp = {
            "key": key,
            "po_line": po_line,
            "invoice_line": inv_line,
            "quantity_match": (po_line and inv_line and abs(po_line["quantity"] - inv_line["quantity"])<=plan["validation_rules"]["line_quantity_tolerance"]),
            "unit_price_match": (po_line and inv_line and abs(po_line["unit_price"] - inv_line["unit_price"])<= (po_line["unit_price"]*plan["validation_rules"]["price_tolerance_pct"]/100.0 if po_line else 0))
        }
        comparisons.append(comp)
    # Step 4: inventory checks
    inventory_trace = []
    for l in po["lines"]:
        item_id = l["item_id"]
        inv_call = call_tool("check_inventory", {"item_id": item_id})
        inventory_trace.append(inv_call)
    trace.extend(inventory_trace)
    result = {
        "trace": trace,
        "comparisons": comparisons,
        "po": po,
        "invoice": inv,
        "plan_seed": plan.get("seed")
    }
    return result
