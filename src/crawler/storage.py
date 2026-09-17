import sqlite3
from pathlib import Path
from .models import Document
class Store:
 def __init__(self,root="data"):
  self.root=Path(root); (self.root/"raw/html").mkdir(parents=True,exist_ok=True); (self.root/"raw/pdf").mkdir(parents=True,exist_ok=True); self.db=sqlite3.connect(self.root/"crawler.db"); self.db.row_factory=sqlite3.Row
  self.db.executescript("CREATE TABLE IF NOT EXISTS documents (document_id TEXT PRIMARY KEY,company_id TEXT,source_id TEXT,document_type TEXT,title TEXT,source_url TEXT,canonical_url TEXT,publisher TEXT,source_tier INTEGER,published_at TEXT,retrieved_at TEXT,http_status INTEGER,content_type TEXT,file_size INTEGER,sha256 TEXT,storage_path TEXT,parent_page_url TEXT); CREATE UNIQUE INDEX IF NOT EXISTS idx_doc_hash ON documents(company_id,sha256); CREATE TABLE IF NOT EXISTS discovered_urls (company_id TEXT,url TEXT PRIMARY KEY,source_id TEXT,title TEXT,document_type TEXT,parent_page_url TEXT);"); self.db.commit()
 def discovered(self,company_id,source_id,rows):
  for r in rows: self.db.execute("INSERT OR IGNORE INTO discovered_urls VALUES (?,?,?,?,?,?)",(company_id,r["url"],source_id,r["title"],r["document_type"],r["parent_page_url"]))
  self.db.commit()
 def save(self,doc:Document,data,kind):
  if self.db.execute("SELECT 1 FROM documents WHERE company_id=? AND sha256=?",(doc.company_id,doc.sha256)).fetchone(): return False
  path=self.root/"raw"/kind/doc.company_id/doc.sha256[:2]/f"{doc.sha256}.{'pdf' if kind=='pdf' else 'html'}"; path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(data); doc.storage_path=str(path); self.db.execute("INSERT INTO documents VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",tuple(doc.dict().values())); self.db.commit(); return True
 def export(self,company_id): return [dict(x) for x in self.db.execute("SELECT * FROM documents WHERE company_id=? ORDER BY retrieved_at",(company_id,))]
 def close(self): self.db.close()
