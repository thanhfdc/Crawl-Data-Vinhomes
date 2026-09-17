from enum import StrEnum
class DocumentType(StrEnum):
 ANNUAL_REPORT="ANNUAL_REPORT"; CORPORATE_GOVERNANCE_REPORT="CORPORATE_GOVERNANCE_REPORT"; PERSONNEL_CHANGE_DISCLOSURE="PERSONNEL_CHANGE_DISCLOSURE"; AGM_DOCUMENT="AGM_DOCUMENT"; AGM_RESOLUTION="AGM_RESOLUTION"; FINANCIAL_REPORT="FINANCIAL_REPORT"; COMPANY_CHARTER="COMPANY_CHARTER"; COMPANY_PROFILE="COMPANY_PROFILE"; OTHER_GOVERNANCE_DOCUMENT="OTHER_GOVERNANCE_DOCUMENT"; UNKNOWN="UNKNOWN"
RULES=[(DocumentType.CORPORATE_GOVERNANCE_REPORT,("corporate governance","governance report","quan tri cong ty")),(DocumentType.ANNUAL_REPORT,("annual report","annual-report","bao cao thuong nien")),(DocumentType.PERSONNEL_CHANGE_DISCLOSURE,("personnel","appointment","dismissal","change of personnel")),(DocumentType.AGM_RESOLUTION,("agm resolution","shareholders resolution","resolution")),(DocumentType.AGM_DOCUMENT,("agm","annual general meeting","shareholders meeting")),(DocumentType.FINANCIAL_REPORT,("financial statement","financial report","bao cao tai chinh")),(DocumentType.COMPANY_CHARTER,("charter","company charter")),(DocumentType.COMPANY_PROFILE,("company profile","business profile"))]
def classify_document(url,title="",anchor_text=""):
 text=f"{url} {title} {anchor_text}".lower()
 for kind,words in RULES:
  if any(w in text for w in words): return kind
 return DocumentType.UNKNOWN
