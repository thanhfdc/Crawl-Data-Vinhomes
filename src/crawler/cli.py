import argparse,asyncio,json,logging
from pathlib import Path
from .config import load_company
from .storage import Store
from .pipeline import run
from .http import HttpClient
from .excel_export import export_excel
logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(message)s")
def main():
 p=argparse.ArgumentParser(); s=p.add_subparsers(dest="command",required=True)
 for n in ("discover","crawl","diagnose"): s.add_parser(n).add_argument("--company",required=True)
 e=s.add_parser("export-excel"); e.add_argument("--company",required=True); e.add_argument("--output")
 s.add_parser("status").add_argument("--company",required=True); e=s.add_parser("export-documents"); e.add_argument("--company",required=True); e.add_argument("--output",required=True)
 a=p.parse_args(); config=load_company(Path("config/companies")/f"{a.company.lower()}.yaml"); store=Store()
 try:
  if a.command in ("discover","crawl"): print(json.dumps(asyncio.run(run(config,store,a.command=="crawl")),ensure_ascii=False,indent=2))
  elif a.command=="diagnose":
   async def check():
    client=HttpClient()
    try:
     return {source.source_id:await client.diagnose(source.base_url) for source in config.sources}
    finally: await client.aclose()
   print(json.dumps(asyncio.run(check()),ensure_ascii=False,indent=2))
  elif a.command=="status": print(json.dumps({"documents":len(store.export(a.company))},indent=2))
  elif a.command=="export-excel":
   output=a.output or str(Path("output")/f"{a.company.upper()}_crawl_export.xlsx")
   print(json.dumps(export_excel(store,config,output),ensure_ascii=False,indent=2))
  else: Path(a.output).write_text(json.dumps(store.export(a.company),ensure_ascii=False,indent=2),encoding="utf-8")
 finally: store.close()
