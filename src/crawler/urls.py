from urllib.parse import urljoin,urlsplit,urlunsplit,parse_qsl,urlencode
import re
TRACKING={"utm_source","utm_medium","utm_campaign","utm_term","utm_content","fbclid"}
def normalize_url(url,base=None):
 p=urlsplit(urljoin(base,url) if base else url); scheme=p.scheme.lower(); host=(p.hostname or "").lower(); path=re.sub(r"/{2,}","/",p.path or "/"); q=urlencode([(k,v) for k,v in parse_qsl(p.query,keep_blank_values=True) if k.lower() not in TRACKING]); return urlunsplit((scheme,host,path,q,""))
