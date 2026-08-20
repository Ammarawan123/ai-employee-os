import os
from typing import Any, Dict, List
import boto3
from elasticsearch import AsyncElasticsearch

# Storage Setup (AWS S3 / Cloudflare R2)
S3_BUCKET = os.getenv("S3_BUCKET_NAME", "ai-employee-docs")
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "mock_key"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "mock_secret"),
    endpoint_url=os.getenv("STORAGE_ENDPOINT_URL"),  # Custom R2 Endpoint
)

# Search Engine Setup
es_client = AsyncElasticsearch(
    hosts=[os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")]
)


async def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """Extracts text using OCR or native PDF parsing."""
    if filename.endswith(".pdf"):
        # PDF parsing logic
        return "Parsed PDF Document Content..."
    # Image OCR logic
    return "Extracted OCR Text Content..."


async def index_document_es(doc_id: int, title: str, text: str):
    """Indexes processed document text into Elasticsearch."""
    doc_body = {"title": title, "content": text, "doc_id": doc_id}
    await es_client.index(index="documents", id=str(doc_id), document=doc_body)


async def search_elasticsearch(keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Performs full-text search using Elasticsearch."""
    query = {"query": {"multi_match": {"query": keyword, "fields": ["title", "content"]}}}
    response = await es_client.search(index="documents", body=query, size=limit)
    return [hit["_source"] for hit in response["hits"]["hits"]]