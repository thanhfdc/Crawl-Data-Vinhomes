from dataclasses import dataclass,asdict
from datetime import datetime,timezone
import hashlib
def now(): return datetime.now(timezone.utc).isoformat()
def sha256(data): return hashlib.sha256(data).hexdigest()
@dataclass
class Document:
 document_id:str; company_id:str; source_id:str; document_type:str; title:str; source_url:str; canonical_url:str; publisher:str; source_tier:int; published_at:str|None; retrieved_at:str; http_status:int; content_type:str; file_size:int; sha256:str; storage_path:str; parent_page_url:str
 def dict(self): return asdict(self)
