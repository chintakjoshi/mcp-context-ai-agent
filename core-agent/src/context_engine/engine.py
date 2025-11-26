from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio
from dataclasses import dataclass
from enum import Enum
import numpy as np

class ContextType(Enum):
    MEETING = "meeting"
    PROJECT = "project"
    TASK = "task"
    COMMUNICATION = "communication"
    HEALTH = "health"

@dataclass
class ContextEntity:
    id: str
    type: ContextType
    content: Dict[str, Any]
    timestamp: datetime
    importance: float  # 0.0 to 1.0
    relationships: List[str]
    embedding: Optional[np.ndarray] = None

class ContextEngine:
    def __init__(self, vector_db, llm_client):
        self.vector_db = vector_db
        self.llm_client = llm_client
        self.active_contexts: Dict[str, ContextEntity] = {}
        self.context_history: List[ContextEntity] = []
        
    async def update_context(self, source: str, data: Dict[str, Any]):
        """Update context from MCP server data"""
        entities = await self._extract_entities(source, data)
        
        for entity in entities:
            # Store in vector DB for semantic search
            await self._store_entity(entity)
            
            # Update active contexts
            self._update_active_contexts(entity)
            
            # Check for proactive alerts
            await self._check_alerts(entity)
    
    async def _extract_entities(self, source: str, data: Dict) -> List[ContextEntity]:
        """Extract meaningful entities from raw data"""
        entities = []
        
        if source == "calendar":
            entities.extend(await self._extract_calendar_entities(data))
        elif source == "gmail":
            entities.extend(await self._extract_email_entities(data))
        elif source == "notion":
            entities.extend(await self._extract_notion_entities(data))
            
        return entities
    
    async def _extract_calendar_entities(self, events: List[Dict]) -> List[ContextEntity]:
        """Extract entities from calendar events"""
        entities = []
        for event in events:
            entity = ContextEntity(
                id=f"calendar_{event['id']}",
                type=ContextType.MEETING,
                content={
                    "title": event.get('summary', ''),
                    "start_time": event['start']['dateTime'],
                    "end_time": event['end']['dateTime'],
                    "participants": event.get('attendees', []),
                    "description": event.get('description', '')
                },
                timestamp=datetime.now(),
                importance=self._calculate_meeting_importance(event),
                relationships=[]
            )
            entities.append(entity)
        return entities
    
    def _calculate_meeting_importance(self, event: Dict) -> float:
        """Calculate importance of a meeting"""
        importance = 0.5  # Base importance
        
        # Factors: duration, participants, recurrence, user interaction
        if len(event.get('attendees', [])) > 5:
            importance += 0.2
        if 'important' in event.get('summary', '').lower():
            importance += 0.3
            
        return min(importance, 1.0)
    
    async def get_relevant_context(self, query: str, limit: int = 5) -> List[ContextEntity]:
        """Get context entities relevant to query"""
        # Semantic search in vector DB
        results = await self.vector_db.similarity_search(query, k=limit)
        return [self._vector_result_to_entity(result) for result in results]
    
    def _update_active_contexts(self, entity: ContextEntity):
        """Update the active context state"""
        self.active_contexts[entity.id] = entity
        self.context_history.append(entity)
        
        # Keep only recent history (e.g., last 1000 entities)
        if len(self.context_history) > 1000:
            self.context_history = self.context_history[-1000:]