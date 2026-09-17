import asyncio, random, time, logging, httpx
log=logging.getLogger("crawler.http")
class HttpClient:
 def __init__(self):
  self.client=httpx.AsyncClient(headers={"User-Agent":"VinhomesOfficialCrawler/0.1"},timeout=30,follow_redirects=True); self.sem=asyncio.Semaphore(4)
 async def get(self,url):
  async with self.sem:
   for attempt in range(1,4):
    started=time.perf_counter()
    try:
     r=await self.client.get(url)
     if r.status_code not in (429,500,502,503,504): return r
     log.error("http failure url=%s status=%s attempt=%s elapsed_ms=%s",url,r.status_code,attempt,round((time.perf_counter()-started)*1000))
    except httpx.HTTPError as exc:
     log.exception("request failure url=%s exception=%s message=%s attempt=%s elapsed_ms=%s",url,type(exc).__name__,exc,attempt,round((time.perf_counter()-started)*1000))
     if attempt==3: raise
    await asyncio.sleep(2**(attempt-1)+random.random()/5)
   return r
 async def diagnose(self,url):
  started=time.perf_counter()
  try:
   r=await self.client.get(url)
   return {"ok":True,"status":r.status_code,"final_url":str(r.url),"content_type":r.headers.get("content-type"),"size":len(r.content),"elapsed_ms":round((time.perf_counter()-started)*1000),"history":[str(x.url) for x in r.history]}
  except Exception as exc:
   log.exception("diagnostic failure url=%s exception=%s message=%s elapsed_ms=%s",url,type(exc).__name__,exc,round((time.perf_counter()-started)*1000))
   return {"ok":False,"exception":type(exc).__name__,"message":str(exc),"elapsed_ms":round((time.perf_counter()-started)*1000)}
 async def aclose(self): await self.client.aclose()
