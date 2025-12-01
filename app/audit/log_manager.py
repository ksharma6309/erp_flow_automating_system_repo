"""
Audit Log Manager:
- Append-only JSONL audit log
- HMAC signing per entry
- Export JSON / CSV
"""
import os
import json
import hmac
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict

LOG_DIR = Path(__file__).parent
LOG_FILE = LOG_DIR / "audit_log.jsonl"
SECRET = os.getenv("AUDIT_HMAC_SECRET", "dev-secret-key")

class AuditLogManager:
    def __init__(self, log_file: Path = LOG_FILE, secret: str = SECRET):
        self.log_file = log_file
        self.secret = secret
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def sign(self, payload: bytes) -> str:
        hm = hmac.new(self.secret.encode(), payload, hashlib.sha256)
        return hm.hexdigest()

    def append_log(self, decision_payload: Dict, extra: Dict = None):
        record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "payload": decision_payload,
            "extra": extra or {}
        }
        payload_bytes = json.dumps(record, sort_keys=True).encode()
        signature = self.sign(payload_bytes)
        entry = {"record": record, "hmac": signature}
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        return entry

    def read_logs(self):
        if not self.log_file.exists():
            return []
        out=[]
        with open(self.log_file,"r",encoding="utf-8") as f:
            for line in f:
                out.append(json.loads(line))
        return out

    def export_json(self, dst: Path):
        logs = self.read_logs()
        dst.write_text(json.dumps(logs, indent=2))
        return dst

    def export_csv(self, dst: Path):
        import csv
        logs = self.read_logs()
        with open(dst,"w",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp","decision","reasons","po_id","invoice_id","hmac"])
            for e in logs:
                rec = e["record"]
                payload = rec["payload"]
                writer.writerow([
                    rec["timestamp"],
                    payload.get("decision"),
                    "|".join(payload.get("reasons",[])),
                    payload.get("po_id"),
                    payload.get("invoice_id"),
                    e.get("hmac")
                ])
        return dst
