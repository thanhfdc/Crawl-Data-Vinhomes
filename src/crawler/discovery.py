from bs4 import BeautifulSoup
from .urls import normalize_url
from .classifier import classify_document
def discover(html,page_url,keywords):
 soup=BeautifulSoup(html,"html.parser"); out=[]
 for a in soup.find_all("a",href=True):
  url=normalize_url(a["href"],page_url); title=a.get("title",""); anchor=" ".join(a.stripped_strings); text=f"{url} {title} {anchor}".lower()
  if any(k.lower() in text for k in keywords) or url.lower().split("?")[0].endswith((".pdf",".html",".htm")):
   out.append({"url":url,"title":anchor or title or url,"document_type":str(classify_document(url,title,anchor)),"parent_page_url":page_url})
 return list({x["url"]:x for x in out}.values())
