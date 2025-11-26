import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any
import json
import logging

class VectorMemory:
    def __init__(self, persist_directory: str = "./data/chroma"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection("context_entities")
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.logger = logging.getLogger(__name__)
    
    async def store_entity(self, entity) -> None:
        """Store entity in vector database"""
        try:
            # Create embedding from entity content
            text_content = self._entity_to_text(entity)
            embedding = self.encoder.encode(text_content)
            
            self.collection.add(
                ids=[entity.id],
                embeddings=[embedding.tolist()],
                metadatas=[{
                    "type": entity.type,
                    "timestamp": entity.timestamp.isoformat(),
                    "importance": entity.importance,
                }],
                documents=[text_content]
            )
            self.logger.info(f"Stored entity: {entity.id}")
        except Exception as e:
            self.logger.error(f"Error storing entity: {e}")
    
    async def similarity_search(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar entities"""
        try:
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
        except Exception as e:
            self.logger.error(f"Error in similarity search: {e}")
            return []
    
    def _entity_to_text(self, entity) -> str:
        """Convert entity to text for embedding"""
        return f"{entity.type}: {entity.content}"