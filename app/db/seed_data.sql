-- #simple PO and Invoice tables
CREATE TABLE IF NOT EXISTS purchase_orders (
  po_id TEXT PRIMARY KEY,
  vendor_id TEXT,
  vendor_name TEXT,
  currency TEXT,
  total_amount REAL
);

CREATE TABLE IF NOT EXISTS po_lines (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  po_id TEXT,
  line_id INTEGER,
  item_id TEXT,
  description TEXT,
  quantity REAL,
  unit_price REAL,
  currency TEXT
);

CREATE TABLE IF NOT EXISTS invoices (
  invoice_id TEXT PRIMARY KEY,
  vendor_id TEXT,
  vendor_name TEXT,
  currency TEXT,
  total_amount REAL
);

CREATE TABLE IF NOT EXISTS invoice_lines (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  invoice_id TEXT,
  line_id INTEGER,
  item_id TEXT,
  description TEXT,
  quantity REAL,
  unit_price REAL,
  currency TEXT
);

CREATE TABLE IF NOT EXISTS inventory (
  item_id TEXT PRIMARY KEY,
  on_hand REAL
);

-- sample: perfect match PO and invoice
INSERT OR IGNORE INTO purchase_orders VALUES ('PO-1001','V-001','Acme Corp','USD',1000.0);
INSERT OR IGNORE INTO po_lines (po_id,line_id,item_id,description,quantity,unit_price,currency) VALUES
('PO-1001',1,'ITEM-01','Widget A',10,50.0,'USD'),
('PO-1001',2,'ITEM-02','Widget B',5,100.0,'USD');

-- invoice perfect match
INSERT OR IGNORE INTO invoices VALUES ('INV-5001','V-001','Acme Corp','USD',1000.0);
INSERT OR IGNORE INTO invoice_lines (invoice_id,line_id,item_id,description,quantity,unit_price,currency) VALUES
('INV-5001',1,'ITEM-01','Widget A',10,50.0,'USD'),
('INV-5001',2,'ITEM-02','Widget B',5,100.0,'USD');

-- mismatch example: prices differ
INSERT OR IGNORE INTO purchase_orders VALUES ('PO-1002','V-002','Beta LLC','USD',1000.0);
INSERT OR IGNORE INTO po_lines (po_id,line_id,item_id,description,quantity,unit_price,currency) VALUES
('PO-1002',1,'ITEM-03','Widget C',10,50.0,'USD'),
('PO-1002',2,'ITEM-04','Widget D',5,100.0,'USD');

INSERT OR IGNORE INTO invoices VALUES ('INV-5002','V-002','Beta LLC','USD',1100.0);
INSERT OR IGNORE INTO invoice_lines (invoice_id,line_id,item_id,description,quantity,unit_price,currency) VALUES
('INV-5002',1,'ITEM-03','Widget C',10,55.0,'USD'), -- price mismatch
('INV-5002',2,'ITEM-04','Widget D',5,100.0,'USD');

-- inventory
INSERT OR IGNORE INTO inventory VALUES ('ITEM-01', 100);
INSERT OR IGNORE INTO inventory VALUES ('ITEM-02', 2);   -- low stock
INSERT OR IGNORE INTO inventory VALUES ('ITEM-03', 50);
INSERT OR IGNORE INTO inventory VALUES ('ITEM-04', 0);
