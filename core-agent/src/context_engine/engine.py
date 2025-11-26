from typing import Dict, List, Any
from datetime import datetime
import asyncio
import logging
from .entities import ContextEntity, ContextType

class ContextEngine:
    def __init__(self, vector_db, llm_client=None):
        self.vector_db = vector_db
        self.llm_client = llm_client
        self.active_contexts: Dict[str, ContextEntity] = {}
        self.context_history: List[ContextEntity] = []
        self.logger = logging.getLogger(__name__)
        
    async def update_context(self, source: str, data: Dict[str, Any]):
        """Update context from data source"""
        self.logger.info(f"Updating context from {source}")
        
        entities = await self._extract_entities(source, data)
        
        for entity in entities:
            await self.vector_db.store_entity(entity)
            self.active_contexts[entity.id] = entity
            self.context_history.append(entity)
            
            # Check for simple alerts
            await self._check_basic_alerts(entity)
    
    async def _extract_entities(self, source: str, data: Dict) -> List[ContextEntity]:
        """Extract entities from raw data - simplified version"""
        entities = []
        
        if source == "calendar":
            entities.extend(await self._extract_calendar_entities(data))
        elif source == "mock":
            # For testing
            entities.extend(await self._extract_mock_entities(data))
            
        return entities
    
    async def _extract_calendar_entities(self, events: List[Dict]) -> List[ContextEntity]:
        """Extract entities from calendar events"""
        entities = []
        for event in events:
            entity = ContextEntity(
                id=f"calendar_{event['id']}",
                type=ContextType.MEETING.value,
                content={
                    "title": event.get('summary', 'Unknown'),
                    "start_time": event.get('start', {}).get('dateTime', ''),
                    "end_time": event.get('end', {}).get('dateTime', ''),
                    "source": "calendar"
                },
                timestamp=datetime.now(),
                importance=0.7,
                relationships=[]
            )
            entities.append(entity)
        return entities
    
    async def _extract_mock_entities(self, data: Dict) -> List[ContextEntity]:
        """Extract entities from mock data for testing"""
        entities = []
        entity = ContextEntity(
            id="mock_1",
            type=ContextType.MEETING.value,
            content={
                "title": "Test Meeting with Acme Corp",
                "start_time": "2024-01-15T14:00:00Z",
                "description": "Quarterly business review",
                "source": "mock"
            },
            timestamp=datetime.now(),
            importance=0.8,
            relationships=[]
        )
        entities.append(entity)
        return entities
    
    async def _check_basic_alerts(self, entity: ContextEntity):
        """Check for basic alert conditions"""
        if entity.type == ContextType.MEETING.value:
            self.logger.info(f"Meeting alert: {entity.content.get('title')}")
    
    async def get_relevant_context(self, query: str, limit: int = 5) -> List[ContextEntity]:
        """Get relevant context for query"""
        results = await self.vector_db.similarity_search(query, limit)
        # Convert back to entities (simplified)
        return results