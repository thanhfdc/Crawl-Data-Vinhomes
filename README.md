# Vinhomes Official Leadership Document Crawler (V1)

Document-first crawler for official Vinhomes (`VHM`) governance evidence. It loads YAML source configuration, discovers relevant links, downloads HTML/PDF content, hashes and deduplicates bytes, and stores provenance in SQLite. It does not extract people, use LLMs, OCR, or crawl third-party media.

## Run

```text
pip install -e ".[test]"
python -m crawler discover --company VHM
python -m crawler crawl --company VHM
python -m crawler status --company VHM
python -m crawler export-documents --company VHM --output documents.json
```

Sources are configured in `config/companies/vhm.yaml`: official Investor Relations, Information Disclosure, Annual Reports, and Financial Statements pages. Raw files are under `data/raw/`; metadata and discovery records are in `data/crawler.db`.

## Test

```text
pytest -q
```

V1 uses generic HTML discovery and deterministic keyword classification. Publication-date extraction, pagination-specific adapters, leadership extraction, and cross-document verification are Phase 2 work.
