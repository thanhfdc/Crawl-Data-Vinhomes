from crawler.urls import normalize_url
from crawler.classifier import classify_document,DocumentType
from crawler.models import sha256
def test_url_normalization(): assert normalize_url("/a//b.pdf?utm_source=x#x","HTTPS://Vinhomes.vn/x")=="https://vinhomes.vn/a/b.pdf"
def test_classification(): assert classify_document("https://x/annual-report-2024.pdf")==DocumentType.ANNUAL_REPORT
def test_hash(): assert sha256(b"abc")=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
