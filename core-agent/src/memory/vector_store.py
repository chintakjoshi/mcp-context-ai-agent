import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any
import json

class VectorMemory:
    def __init__(self, persist_directory: str = "./data/chroma"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection("context_entities")
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
    
    async def store_entity(self, entity) -> None:
        """Store entity in vector database"""
        # Create embedding from entity content
        text_content = self._entity_to_text(entity)
        embedding = self.encoder.encode(text_content)
        
        self.collection.add(
            ids=[entity.id],
            embeddings=[embedding.tolist()],
            metadatas=[{
                "type": entity.type.value,
                "timestamp": entity.timestamp.isoformat(),
                "importance": entity.importance,
                "content": json.dumps(entity.content)
            }],
            documents=[text_content]
        )
    
    async def similarity_search(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar entities"""
        query_embedding = self.encoder.encode(query).tolist()
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["metadatas", "documents", "distances"]
        )
        
        return [
            {
                "id": results["ids"][0][i],
                "metadata": results["metadatas"][0][i],
                "document": results["documents"][0][i],
                "distance": results["distances"][0][i]
            }
            for i in range(len(results["ids"][0]))
        ]
    
    def _entity_to_text(self, entity) -> str:
        """Convert entity to text for embedding"""
        content_str = json.dumps(entity.content)
        return f"{entity.type.value}: {content_str}"