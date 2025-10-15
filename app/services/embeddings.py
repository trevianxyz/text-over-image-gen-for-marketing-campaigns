"""Embeddings service"""
from typing import Any, Dict
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB
client = chromadb.Client(Settings(persist_directory="db/chroma"))
collection = client.get_or_create_collection("campaign_assets")

# MiniLM embeddings
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_and_store(campaign_id: str, text: str, metadata: dict):
    vec = model.encode(text).tolist()
    collection.add(ids=[campaign_id], embeddings=[vec], metadatas=[metadata], documents=[text])

def search_similar(query: str, top_k: int = 3) -> Dict[str, Any]:
    """
    Search for similar campaigns using vector embeddings
    """
    vec = model.encode(query).tolist()
    return collection.query(query_embeddings=[vec], n_results=top_k)