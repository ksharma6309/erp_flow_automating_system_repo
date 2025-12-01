import streamlit as st
from pathlib import Path
import json, time, os, hmac, hashlib, csv, io
import pandas as pd

# -------------------- Page config & styling --------------------
st.set_page_config(page_title=" 📊 ERP Flow Automator", layout="wide")
CSS = """
<style>
.status-box { background:#0f172a; padding:18px; border-radius:12px; color:white; }
.green-dot { height:10px; width:10px; background:#22c55e; border-radius:50%; display:inline-block; margin-right:8px; }
.module-examples { margin-bottom:12px; }
.example-btn { margin-right:8px; margin-bottom:8px; }
.table-row { padding:8px 0; border-bottom:1px solid #eee; display:flex; align-items:center; }
.table-header { font-weight:600; padding:10px 0; }
.small-muted { color:#6b7280; font-size:13px; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# -------------------- Audit/Logging utilities --------------------
ROOT = Path(__file__).parent
AUDIT_DIR = ROOT / "audit"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_LOG = AUDIT_DIR / "audit_log.jsonl"
HMAC_SECRET = os.getenv("AUDIT_HMAC_SECRET", "dev-secret-key")
SETTINGS_FILE = AUDIT_DIR / "settings.json"
INVENTORY_FILE = AUDIT_DIR / "inventory.json"

if INVENTORY_FILE.exists():
    try:
        text = INVENTORY_FILE.read_text(encoding="utf-8")
        loaded = json.loads(text)
        if isinstance(loaded, dict):
            INVENTORY = loaded
        else:
            raise ValueError("inventory.json does not contain an object")
    except Exception as e:
        st.warning(f"Could not read inventory file (will recreate): {e}")
        try:
            INVENTORY_FILE.write_text() #json.dumps(INVENTORY, indent=2), encoding="utf-8")
        except Exception:
            pass
else:
    try:
        INVENTORY_FILE.write_text() # json.dumps(INVENTORY, indent=2), encoding="utf-8")
    except Exception:
        pass


def save_inventory_to_file(inv_dict):
    INVENTORY_FILE.write_text(json.dumps(inv_dict, indent=2), encoding="utf-8")

def hmac_sign(obj_bytes: bytes) -> str:
    return hmac.new(HMAC_SECRET.encode(), obj_bytes, hashlib.sha256).hexdigest()

def append_audit(action: str, payload: dict):
    entry = {"timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "action": action, "payload": payload}
    raw = json.dumps(entry, sort_keys=True).encode()
    sig = hmac_sign(raw)
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({"record": entry, "hmac": sig}) + "\n")

def read_audit(limit=500):
    if not AUDIT_LOG.exists():
        return []
    with open(AUDIT_LOG, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    out=[]
    for line in lines[-limit:]:
        try:
            out.append(json.loads(line))
        except Exception:
            continue
    return out

def payload_summary(payload, max_len=120):
    try:
        s = json.dumps(payload, separators=(",", ":"), default=str)
    except Exception:
        s = str(payload)
    return s if len(s) <= max_len else s[:max_len-3]+"..."

def download_json(obj, filename):
    return st.download_button(label=f"Download {filename}", data=json.dumps(obj, indent=2), file_name=filename, mime="application/json")

# -------------------- Sample datasets (from earlier) --------------------
PO_DB = {
    "PO-1001": {"po_id":"PO-1001","vendor_id":"V-001","vendor_name":"Acme Corp","currency":"USD","total_amount":1000.0,
        "lines":[{"line_id":1,"item_id":"ITEM-01","description":"Widget A","quantity":10,"unit_price":50.0,"currency":"USD"},
                 {"line_id":2,"item_id":"ITEM-02","description":"Widget B","quantity":5,"unit_price":100.0,"currency":"USD"}]},
    "PO-1002": {"po_id":"PO-1002","vendor_id":"V-002","vendor_name":"Beta LLC","currency":"USD","total_amount":1000.0,
        "lines":[{"line_id":1,"item_id":"ITEM-03","description":"Widget C","quantity":10,"unit_price":50.0,"currency":"USD"},
                 {"line_id":2,"item_id":"ITEM-04","description":"Widget D","quantity":5,"unit_price":100.0,"currency":"USD"}]}
}
INV_DB = {
    "INV-5001": {"invoice_id":"INV-5001","vendor_id":"V-001","vendor_name":"Acme Corp","currency":"USD","region":"US","total_amount":1000.0,
        "lines":[{"line_id":1,"item_id":"ITEM-01","description":"Widget A","quantity":10,"unit_price":50.0,"currency":"USD"},
                 {"line_id":2,"item_id":"ITEM-02","description":"Widget B","quantity":5,"unit_price":100.0,"currency":"USD"}]},
    "INV-5002": {"invoice_id":"INV-5002","vendor_id":"V-002","vendor_name":"Beta LLC","currency":"USD","region":"US","total_amount":1100.0,
        "lines":[{"line_id":1,"item_id":"ITEM-03","description":"Widget C","quantity":10,"unit_price":55.0,"currency":"USD"},
                 {"line_id":2,"item_id":"ITEM-04","description":"Widget D","quantity":5,"unit_price":100.0,"currency":"USD"}]},
    "INV-GST-100": {"invoice_id":"INV-GST-100","vendor_id":"V-010","vendor_name":"India Supplies","currency":"INR","region":"IN","total_amount":11800.0,"place_of_supply":"KA",
        "lines":[{"line_id":1,"item_id":"ITEM-G1","description":"Industrial Widget A","quantity":10,"unit_price":1000.0,"currency":"INR","hsn":"8471","gst_rate":18}]}
}
GRN_DB = {
    "GRN-7001":{"grn_id":"GRN-7001","po_id":"PO-1001","invoice_id":"INV-5001","received_lines":[{"line_id":1,"item_id":"ITEM-01","received_qty":10},{"line_id":2,"item_id":"ITEM-02","received_qty":5}],"status":"RECEIVED"},
    "GRN-7002":{"grn_id":"GRN-7002","po_id":"PO-1002","invoice_id":None,"received_lines":[{"line_id":1,"item_id":"ITEM-03","received_qty":10},{"line_id":2,"item_id":"ITEM-04","received_qty":4}],"status":"PARTIAL"}
}
INVENTORY = {"ITEM-01":{"item_id":"ITEM-01","description":"Widget A","on_hand":100},
             "ITEM-02":{"item_id":"ITEM-02","description":"Widget B","on_hand":2},
             "ITEM-03":{"item_id":"ITEM-03","description":"Widget C","on_hand":50},
             "ITEM-04":{"item_id":"ITEM-04","description":"Widget D","on_hand":0}}

# initial audit log
#append_audit("system_start", {"msg":"ERP Quick Examples UI started"})

# -------------------- Planner / Executor / Auditor --------------------
def planner_generate(invoice_id, po_id):
    seed = abs(hash(f"{invoice_id}:{po_id}")) % (10**9)
    return {"invoice_id": invoice_id, "po_id": po_id, "seed": seed,
            "steps":[{"id":1,"name":"fetch_po"},{"id":2,"name":"fetch_invoice"},{"id":3,"name":"compare_lines"},{"id":4,"name":"check_inventory"},{"id":5,"name":"audit_decision"}],
            "validation_rules":{"price_tolerance_pct":0.0,"quantity_tolerance":0.0}}

def executor_run(plan):
    trace=[]
    po = PO_DB.get(plan["po_id"])
    inv = INV_DB.get(plan["invoice_id"])
    trace.append({"tool":"get_purchase_order","status":"OK" if po else "NOT_FOUND","response":po})
    trace.append({"tool":"get_invoice","status":"OK" if inv else "NOT_FOUND","response":inv})

    comparisons=[]
    if po and inv:
        po_map = {(l["line_id"],l["item_id"]):l for l in po["lines"]}
        inv_map = {(l["line_id"],l["item_id"]):l for l in inv["lines"]}
        keys = sorted(set(po_map.keys())|set(inv_map.keys()))
        for k in keys:
            p = po_map.get(k); q = inv_map.get(k)
            c = {"key":k,"po_line":p,"invoice_line":q}
            if p and q:
                c["quantity_match"] = abs(p["quantity"]-q["quantity"])<=plan["validation_rules"]["quantity_tolerance"]
                c["unit_price_match"] = abs(p["unit_price"]-q["unit_price"]) <= (p["unit_price"]*plan["validation_rules"]["price_tolerance_pct"]/100.0)
            else:
                c["quantity_match"]=False; c["unit_price_match"]=False
            comparisons.append(c)
    inv_checks = []
    if po:
        for l in po["lines"]:
            item = INVENTORY.get(l["item_id"])
            inv_checks.append({"tool":"check_inventory","item_id":l["item_id"],"response":item})
    trace.append({"tool":"compare","status":"COMPLETE","response":comparisons})
    trace.append({"tool":"inventory_checks","status":"COMPLETE","response":inv_checks})
    return {"trace":trace,"po":po,"invoice":inv,"comparisons":comparisons}

def auditor_decide(exec_result):
    reasons=[]
    po = exec_result.get("po"); inv = exec_result.get("invoice")
    if not po: reasons.append("po_not_found")
    if not inv: reasons.append("invoice_not_found")
    if po and inv and abs(po.get("total_amount",0)-inv.get("total_amount",0))>0.0001:
        reasons.append("total_mismatch")
    for c in exec_result.get("comparisons",[]):
        if c.get("po_line") is None or c.get("invoice_line") is None:
            reasons.append("missing_line")
        else:
            if not c.get("quantity_match"): reasons.append("quantity_mismatch")
            if not c.get("unit_price_match"): reasons.append("price_mismatch")
    decision = "APPROVE" if not reasons else "ESCALATE"
    result = {"decision":decision,"reasons":sorted(set(reasons))}
    append_audit("audit_decision", {"po":po and po.get("po_id"), "invoice":inv and inv.get("invoice_id"), "decision":result})
    return result

# -------------------- Tax engine --------------------
def compute_tax_for_invoice(invoice):
    region = invoice.get("region","US")
    items = invoice.get("lines", [])
    out_items=[]; total_tax=0.0; total_amount=0.0
    if region=="IN":
        for it in items:
            amt = it["quantity"]*it["unit_price"]
            gst = it.get("gst_rate",18)
            tax_amount = round(amt*gst/100.0,2)
            cgst = round(tax_amount/2,2); sgst = round(tax_amount/2,2)
            out_items.append({**it,"tax_system":"GST","gst_rate":gst,"tax_amount":tax_amount,"cgst":cgst,"sgst":sgst,"net":amt+tax_amount})
            total_tax += tax_amount; total_amount += amt
    else:
        for it in items:
            amt = it["quantity"]*it["unit_price"]
            tax_amount = round(amt*7.0/100.0,2)
            out_items.append({**it,"tax_system":"SalesTax","tax_amount":tax_amount,"net":amt+tax_amount})
            total_tax += tax_amount; total_amount += amt
    result = {"invoice_id":invoice.get("invoice_id"), "region":region, "items":out_items, "total_tax":round(total_tax,2), "subtotal":round(total_amount,2), "grand_total":round(total_amount+total_tax,2)}
    append_audit("tax_calc", {"invoice_id":invoice.get("invoice_id"), "result":{"total_tax":result["total_tax"], "grand_total":result["grand_total"]}})
    return result

# -------------------- Session state helpers for quick examples --------------------
if "run_matching_now" not in st.session_state: st.session_state["run_matching_now"]=False
if "run_grn_now" not in st.session_state: st.session_state["run_grn_now"]=False
if "run_tax_now" not in st.session_state: st.session_state["run_tax_now"]=False
if "run_inventory_now" not in st.session_state: st.session_state["run_inventory_now"]=False

def set_matching_example(inv, po, qty_tol=0, price_tol=0.0):
    st.session_state["inv_id"]=inv
    st.session_state["po_id"]=po
    st.session_state["qty_tol"]=qty_tol
    st.session_state["price_tol_pct"]=price_tol
    st.session_state["run_matching_now"]=True

def set_grn_example(grn):
    st.session_state["grn_id"]=grn
    st.session_state["run_grn_now"]=True

def set_tax_example(inv):
    st.session_state["tax_invoice"]=inv
    st.session_state["run_tax_now"]=True

def set_inventory_example(sku):
    st.session_state["sku"]=sku
    st.session_state["run_inventory_now"]=True

# -------------------- Sidebar & menu --------------------
st.sidebar.title("ERP Agents")
menu = st.sidebar.radio("PAGES", ["Home","Invoice–PO Matching","GRN Checker","Tax Calculator","Inventory Checker","Logs & Settings"])

# -------------------- Home --------------------
if menu == "Home":
    st.title("ERP Flow Automator: Intelligent Task Execution Agent")
    st.write(
        "Welcome to the centralized control plane for your autonomous financial agents. "
        "Monitor, plan, and execute audits across your enterprise resource systems."
    )

    col1, col2, col3,col4 = st.columns(4)

    with col1:
        st.markdown("### 📄 PO - Invoice Matching")
        st.markdown("Automated 3-way matching of Invoices, POs, and Receipts.")
        st.button("Open Module")
        

    with col2:
        st.markdown("### 📦 Inventory Check")
        st.markdown("Reconcile system counts with physical logs.")
        st.button("Open Inventory")
        
    with col3:
        st.markdown("### 📥 GRN Checker")
        st.markdown("Verify GRN details against POs and Invoices.")
        st.button("Open GRN")

    with col4:
        st.markdown("### 💰 Tax Calculator")
        st.markdown("Verify tax codes against regional regulations.")
        st.button("Open Taxes")
    
    st.markdown("---")
        
    st.markdown(
        """
        <div class='status-box'>
            <h3>System Status</h3>
            <span class='green-dot'></span> Planner Agent: Online  
            <span class='green-dot'></span> Audit Agent: Online  
            <span class='green-dot'></span> ERP Connector: Active
        </div>
        """,
        unsafe_allow_html=True,
    )

# -------------------- Invoice–PO Matching --------------------
elif menu=="Invoice–PO Matching":
    st.title("Invoice ↔ PO Matching")
    st.markdown("Quick examples help simulate matched / mismatched scenarios.")

    st.markdown("**Quick examples (page-specific)**")
    c1,c2,c3 = st.columns([1,1,1])
    with c1:
        if st.button("Matched — INV-5001 / PO-1001", key="ex_match"):
            set_matching_example("INV-5001", "PO-1001", qty_tol=0, price_tol=0.0)
    with c2:
        if st.button("Mismatched — INV-5002 / PO-1001", key="ex_mismatch"):
            set_matching_example("INV-5002", "PO-1001", qty_tol=0, price_tol=0.0)
    with c3:
        if st.button("Partial lines — INV-5002 / PO-1002", key="ex_partial"):
            set_matching_example("INV-5002","PO-1002", qty_tol=0, price_tol=0.0)

    # Inputs (bind to session state so quick examples fill them)
    inv_id = st.text_input("Invoice ID", value=st.session_state.get("inv_id","INV-5001"), key="inv_id")
    po_id = st.text_input("Purchase Order ID", value=st.session_state.get("po_id","PO-1001"), key="po_id")
    st.markdown("**Matching rules**")
    qty_tol = st.number_input("Quantity tolerance (absolute)", value=int(st.session_state.get("qty_tol",0)), step=1, key="qty_tol")
    price_tol_pct = st.number_input("Price tolerance (%)", value=float(st.session_state.get("price_tol_pct",0.0)), step=0.1, key="price_tol_pct")

    run_now = False
    if st.button("Generate Plan & Run", key="run_matching_btn"):
        run_now = True
    if st.session_state.get("run_matching_now"):
        run_now = True
        st.session_state["run_matching_now"] = False  

    if run_now:
        plan = planner_generate(inv_id, po_id)
        plan["validation_rules"]["quantity_tolerance"] = qty_tol
        plan["validation_rules"]["price_tolerance_pct"] = price_tol_pct
        st.subheader("Execution Plan")
        st.json(plan)

        exec_res = executor_run(plan)
        st.subheader("Executor Trace")
        st.json(exec_res["trace"])

        matched=[]; unmatched=[]
        for c in exec_res.get("comparisons",[]):
            key = c.get("key"); line_id,item_id = (key if isinstance(key,(list,tuple)) else (None,None))
            p = c.get("po_line"); q = c.get("invoice_line")
            row = {"line_id":line_id,"item_id":item_id,
                   "po_qty": p.get("quantity") if p else None, "inv_qty": q.get("quantity") if q else None,
                   "po_unit_price": p.get("unit_price") if p else None, "inv_unit_price": q.get("unit_price") if q else None,
                   "quantity_match": c.get("quantity_match"), "unit_price_match": c.get("unit_price_match"),
                   "both_present": bool(p and q)}
            if p and q and c.get("quantity_match") and c.get("unit_price_match"):
                matched.append(row)
            else:
                unmatched.append(row)

        st.subheader(f"Matched lines ({len(matched)})")
        if matched:
            st.table(pd.DataFrame(matched))
            st.download_button("Download matched CSV", data=pd.DataFrame(matched).to_csv(index=False), file_name=f"{inv_id}_{po_id}_matched.csv")
            download_json(matched, f"{inv_id}_{po_id}_matched.json")
        else:
            st.info("No matched lines.")

        st.subheader(f"Unmatched lines ({len(unmatched)})")
        if unmatched:
            st.table(pd.DataFrame(unmatched))
            st.download_button("Download unmatched CSV", data=pd.DataFrame(unmatched).to_csv(index=False), file_name=f"{inv_id}_{po_id}_unmatched.csv")
            download_json(unmatched, f"{inv_id}_{po_id}_unmatched.json")
        else:
            st.success("No unmatched lines.")

        audit_res = auditor_decide(exec_res)
        st.subheader("Auditor Decision")
        if audit_res["decision"]=="APPROVE":
            st.success(audit_res)
        else:
            st.warning(audit_res)

        append_audit("run_matching", {"invoice":inv_id,"po":po_id,"matched":len(matched),"unmatched":len(unmatched)})

# -------------------- GRN Checker --------------------
elif menu=="GRN Checker":
    st.title("GRN Checker")
    st.markdown("Quick examples to validate GRNs.")
    c1,c2 = st.columns(2)
    with c1:
        if st.button("GRN OK — GRN-7001"):
            set_grn_example("GRN-7001")
    with c2:
        if st.button("GRN Partial — GRN-7002"):
            set_grn_example("GRN-7002")

    grn_id = st.text_input("GRN ID", value=st.session_state.get("grn_id","GRN-7001"), key="grn_id")
    run_now = False
    if st.button("Validate GRN", key="run_grn_btn"):
        run_now = True
    if st.session_state.get("run_grn_now"):
        run_now = True
        st.session_state["run_grn_now"] = False

    if run_now:
        grn = GRN_DB.get(grn_id)
        if not grn:
            st.warning("GRN not found")
            append_audit("grn_validate", {"grn":grn_id,"result":"not_found"})
        else:
            po = PO_DB.get(grn.get("po_id"))
            inv = INV_DB.get(grn.get("invoice_id")) if grn.get("invoice_id") else None
            res = {"grn":grn,"po":po,"invoice":inv}
            st.json(res)
            append_audit("grn_validate", {"grn":grn_id,"result":"ok","po":grn.get("po_id"),"invoice":grn.get("invoice_id")})
            download_json(res, f"{grn_id}_validation.json")

# -------------------- Tax Calculator --------------------
elif menu=="Tax Calculator":
    st.title("Tax Calculator")
    st.markdown("Quick examples for tax scenarios.")
    c1,c2 = st.columns(2)
    with c1:
        if st.button("IN GST — INV-GST-100"):
            set_tax_example("INV-GST-100")
    with c2:
        if st.button("US SalesTax — INV-5002"):
            set_tax_example("INV-5002")

    tax_invoice = st.text_input("Invoice Number", value=st.session_state.get("tax_invoice","INV-GST-100"), key="tax_invoice")
    run_now = False
    if st.button("Calculate Tax", key="run_tax_btn"):
        run_now = True
    if st.session_state.get("run_tax_now"):
        run_now = True
        st.session_state["run_tax_now"]=False

    if run_now:
        inv = INV_DB.get(tax_invoice)
        if not inv:
            st.warning("Invoice not found")
            append_audit("tax_calc", {"invoice":tax_invoice,"result":"not_found"})
        else:
            t = compute_tax_for_invoice(inv)
            st.json(t)
            append_audit("tax_calc_ui", {"invoice":tax_invoice,"result":"ok"})
            download_json(t, f"{tax_invoice}_tax.json")

# -------------------- Inventory Checker --------------------
elif menu == "Inventory Checker":
    st.title("📦 Inventory Checker")
    st.markdown("Quick stock examples.")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Stock Short — ITEM-01"):
            set_inventory_example("ITEM-01")
    with c2:
        if st.button("Stock OK — ITEM-04"):
            set_inventory_example("ITEM-04")

    sku = st.text_input("Item SKU",
                        value=st.session_state.get("sku", "ITEM-01"),
                        key="sku")

    run_now = False
    if st.button("Check Stock", key="run_inventory_btn"):
        run_now = True
    if st.session_state.get("run_inventory_now"):
        run_now = True
        st.session_state["run_inventory_now"] = False

    if run_now:
        item = INVENTORY.get(sku)

        if not item:
            st.warning("Item not found")
            append_audit("inventory_check",{"item": sku, "result": "not_found"})

        else:
            # Demo: reduce physical stock by 1
            physical = item["on_hand"] if item["on_hand"] == 0 else item["on_hand"] - 1
            mismatch = (physical != item["on_hand"])

            result = {
                "item": item.copy(),
                "physical_count": physical,
                "variance": item["on_hand"] - physical,
                "mismatch": mismatch
            }
            st.json(result)

            append_audit("inventory_check",{"item": sku, "system": item["on_hand"], "physical": physical})

            if mismatch:
                if st.button("Adjust System Stock to Physical", key=f"adj_{sku}"):
                    INVENTORY[sku]["on_hand"] = physical

                    try:
                        save_inventory_to_file(INVENTORY)
                        append_audit("inventory_adjust",{"item": sku, "new_on_hand": physical, "persisted": True})
                        st.success(f"Stock updated to {physical} and saved ✔")
                    except Exception as e:
                        append_audit("inventory_adjust",{"item": sku, "new_on_hand": physical, "persisted": False})
                        st.warning(f"Could not save inventory file: {e}")

                    st.experimental_rerun()

            download_json(result, f"{sku}_stock.json")
            

# -------------------- Logs & Settings --------------------
elif menu=="Logs & Settings":
    HMAC_SECRET = os.getenv("AUDIT_HMAC_SECRET", "dev-secret-key")
    def hmac_sign(obj_bytes: bytes) -> str:
        return hmac.new(HMAC_SECRET.encode(), obj_bytes, hashlib.sha256).hexdigest()

    def append_audit(action: str, payload: dict):
        """
        Append a single audit line. NOTE: this snippet does NOT write a startup 'system_start' record.
        Use this when saving settings or other user actions you want logged.
        """
        entry = {"timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "action": action,
                "payload": payload}
        raw = json.dumps(entry, sort_keys=True).encode()
        sig = hmac_sign(raw)
        with open(AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps({"record": entry, "hmac": sig}) + "\n")

    # --- Read audit lines ---
    def read_audit(limit=500):
        if not AUDIT_LOG.exists():
            return []
        out = []
        with open(AUDIT_LOG, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        for line in lines[-limit:]:
            try:
                out.append(json.loads(line))
            except Exception:
                continue
        return out

    def payload_summary(payload, max_len=140):
        try:
            s = json.dumps(payload, separators=(",", ":"), default=str)
        except Exception:
            s = str(payload)
        return s if len(s) <= max_len else s[:max_len-3] + "..."

    def get_module_from_entry(entry):
        """
        Look at action and payload keys to guess module.
        Returns friendly module name (string).
        """
        rec = entry.get("record", {}) if isinstance(entry, dict) else {}
        action = (rec.get("action") or "").lower()
        payload = rec.get("payload") or {}

        if "tax" in action:
            return "Tax Calculator"
        if "grn" in action:
            return "GRN Checker"
        if "inventory" in action or "stock" in action:
            return "Inventory Checker"
        if "matching" in action or "invoice" in action or "po" in action or "audit" in action:
            return "Invoice–PO Matching"

        keys = " ".join([str(k).lower() for k in (payload.keys() if isinstance(payload, dict) else [])])
        if "invoice" in keys and "po" in keys:
            return "Invoice–PO Matching"
        if "grn" in keys:
            return "GRN Checker"
        if "item" in keys or "sku" in keys or "stock" in keys:
            return "Inventory Checker"
        if "gst" in keys or "tax" in keys or "vat" in keys:
            return "Tax Calculator"

        return action or "Unknown"

    # --- Settings load/save helpers ---
    DEFAULT_SETTINGS = {
        "planner_enabled": True,
        "audit_enabled": True,
        "auto_sync": True
    }

    def load_settings():
        if SETTINGS_FILE.exists():
            try:
                return json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
            except Exception:
                return DEFAULT_SETTINGS.copy()
        return DEFAULT_SETTINGS.copy()

    def save_settings(settings):
        SETTINGS_FILE.write_text(json.dumps(settings, indent=2), encoding="utf-8")

        append_audit("settings_update", {"new_settings": settings})

    # -------------------- UI: Logs & Settings --------------------
    st.title("⚙ Logs & Settings")

    logs = read_audit(limit=500)
    st.markdown(f"**Total log entries:** {len(logs)}")
    st.markdown("Below is a compact tabular list of recent log entries. Use the **View JSON** button to open the full entry.")

    # Table header
    cols = st.columns([2,2,3,8,1])
    cols[0].markdown("**#**")
    cols[1].markdown("**timestamp**")
    cols[2].markdown("**module**")
    cols[3].markdown("**payload_summary**")
    cols[4].markdown("")

    N = 50
    recent = logs[-N:] if len(logs) >= N else logs
    for display_idx, entry in enumerate(reversed(recent), start=1):
        original_index = len(logs) - (display_idx) 
        rec = entry.get("record", {})
        ts = rec.get("timestamp", "")
        action = rec.get("action", "")
        payload = rec.get("payload", {})
        summary = payload_summary(payload, max_len=140)
        module_name = get_module_from_entry(entry)

        c0, c1, c2, c3, c4 = st.columns([0.4, 2, 2, 9, 1])
        c0.write(original_index)
        c1.write(ts)
        c2.write(module_name)
        c3.write(summary)
        if c4.button("View JSON", key=f"view_{original_index}"):
            with st.expander(f"Log JSON — {ts} — {action}", expanded=True):
                st.json(entry)

    st.markdown("---")

    # --- Quick downloads / utilities ---
    st.subheader("Downloads")
    dl_col1, dl_col2 = st.columns(2)
    with dl_col1:
        if st.button("Download all logs (JSON)"):
            st.download_button("Download JSON", data=json.dumps(logs, indent=2), file_name="audit_logs.json", mime="application/json")
    with dl_col2:
        if st.button("Download last 200 logs (CSV)"):
            csv_buf = io.StringIO()
            writer = csv.writer(csv_buf)
            writer.writerow(["timestamp", "action", "payload", "hmac"])
            for e in logs[-200:]:
                rec = e.get("record", {})
                writer.writerow([rec.get("timestamp"), rec.get("action"), json.dumps(rec.get("payload")), e.get("hmac")])
            st.download_button("Download CSV", data=csv_buf.getvalue(), file_name="audit_logs.csv", mime="text/csv")

    st.markdown("---")

    # -------------------- Settings form with Save --------------------
    st.subheader("Settings")
    current_settings = load_settings()

    with st.form("settings_form"):
        planner_enabled = st.checkbox("Enable Planner Agent", value=current_settings.get("planner_enabled", True))
        audit_enabled = st.checkbox("Enable Audit Agent", value=current_settings.get("audit_enabled", True))
        auto_sync = st.checkbox("Allow ERP Connector Auto-Sync", value=current_settings.get("auto_sync", True))
        submitted = st.form_submit_button("Save Settings")

    if submitted:
        new_settings = {
            "planner_enabled": bool(planner_enabled),
            "audit_enabled": bool(audit_enabled),
            "auto_sync": bool(auto_sync)
        }
        save_settings(new_settings)
        st.success("Settings saved.")
   
        current_settings = new_settings

    #st.caption("Settings are persisted to the audit/settings.json file. Settings updates are appended to the audit log.")
    
# -------------------- Footer --------------------
st.markdown("---")
