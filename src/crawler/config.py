from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
import yaml
@dataclass(frozen=True)
class Source:
    source_id:str; company_id:str; name:str; base_url:str; domain:str; source_type:str; source_tier:int; enabled:bool=True
@dataclass(frozen=True)
class CompanyConfig:
    company_id:str; legal_name:str; english_name:str; ticker:str; exchange:str; country:str; sources:tuple[Source,...]; keywords:tuple[str,...]
def load_company(path):
    raw=yaml.safe_load(Path(path).read_text(encoding="utf-8")); c=raw["company"]
    ss=tuple(Source(s["id"],c["id"],s["name"],s["base_url"],urlparse(s["base_url"]).netloc.lower(),s["source_type"],int(s["tier"]),s.get("enabled",True)) for s in raw["sources"])
    return CompanyConfig(c["id"],c["legal_name"],c["english_name"],c["ticker"],c["exchange"],c["country"],ss,tuple(raw["keywords"]["relevant"]))
