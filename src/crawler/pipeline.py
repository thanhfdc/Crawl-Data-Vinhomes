import uuid,logging
from .models import Document,now,sha256
from .urls import normalize_url
from .discovery import discover
async def run(config,store,download=True):
 from .http import HttpClient
 client=HttpClient(); stats={"sources_processed":0,"urls_discovered":0,"documents_downloaded":0,"documents_skipped":0,"documents_failed":0}
 try:
  for source in config.sources:
   if not source.enabled: continue
   stats["sources_processed"]+=1
   try:
    response=await client.get(source.base_url); rows=discover(response.content,str(response.url),config.keywords); stats["urls_discovered"]+=len(rows); store.discovered(config.company_id,source.source_id,rows)
    if not download: continue
    for row in rows:
     try:
      r=await client.get(row["url"]); data=r.content; ctype=r.headers.get("content-type","").split(";")[0].lower(); is_pdf=data.startswith(b"%PDF") or ctype=="application/pdf"; kind="pdf" if is_pdf else "html"
      if is_pdf and len(data)<100: raise ValueError("invalid PDF")
      doc=Document("doc_"+uuid.uuid4().hex,config.company_id,source.source_id,row["document_type"],row["title"],row["url"],normalize_url(row["url"]),"Vinhomes",source.source_tier,None,now(),r.status_code,ctype,len(data),sha256(data),"",row["parent_page_url"])
      if store.save(doc,data,kind): stats["documents_downloaded"]+=1
      else: stats["documents_skipped"]+=1
     except Exception:
      logging.getLogger("crawler.pipeline").exception("document failed source=%s url=%s",source.source_id,row.get("url")); stats["documents_failed"]+=1
   except Exception:
    logging.getLogger("crawler.pipeline").exception("source failed source=%s url=%s",source.source_id,source.base_url); stats["documents_failed"]+=1
 finally: await client.aclose()
 return stats
