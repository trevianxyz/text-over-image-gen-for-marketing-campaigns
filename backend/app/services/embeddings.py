"""Embeddings service"""
from typing import Any, Dict
import chromadb
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB with persistence
client = chromadb.PersistentClient(path="db/chroma")
# Use cosine distance for better similarity scoring (returns values 0-2, where 0 = identical)
collection = client.get_or_create_collection(
    name="campaign_assets",
    metadata={"hnsw:space": "cosine"}  # Cosine distance
)

# MiniLM embeddings
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_and_store(campaign_id: str, text: str, metadata: dict):
    import json
    # Convert list values to JSON strings and filter None values for ChromaDB compatibility
    clean_metadata = {}
    for key, value in metadata.items():
        if value is None:
            continue  # Skip None values
        elif isinstance(value, list):
            clean_metadata[key] = json.dumps(value)
        else:
            clean_metadata[key] = value
    
    # Create rich text for embedding that includes message, country, and audience
    country_name = metadata.get('country_name', '')
    audience = metadata.get('audience', '')
    products = metadata.get('products', [])
    products_str = ', '.join(products) if isinstance(products, list) else str(products)
    
    # Concatenate for better semantic search
    rich_text = f"{text}. Target: {audience} in {country_name}. Products: {products_str}"
    
    vec = model.encode(rich_text).tolist()
    collection.add(ids=[campaign_id], embeddings=[vec], metadatas=[clean_metadata], documents=[text])

def search_similar(query: str, top_k: int = 3) -> Dict[str, Any]:
    """
    Search for similar campaigns using vector embeddings
    """
    vec = model.encode(query).tolist()
    return collection.query(query_embeddings=[vec], n_results=top_k)