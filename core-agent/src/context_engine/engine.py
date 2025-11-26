from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio
import logging
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

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
        elif source == "demo":
            entities.extend(await self._extract_calendar_entities(data.get('events', [])))
            
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
    
    async def get_relevant_context(self, query: str, limit: int = 5) -> List[Dict]:
        """Get relevant context for query"""
        results = await self.vector_db.similarity_search(query, limit)
        return results
    
    async def check_meeting_alerts(self) -> List[Dict]:
        """Check for meeting alerts - simple version"""
        alerts = []
        
        # Get upcoming meetings
        upcoming = await self.get_relevant_context("meeting", 10)
        
        for item in upcoming:
            metadata = item.get('metadata', {})
            if metadata.get('type') == 'meeting':
                content = metadata.get('content', {})
                title = content.get('title', 'Unknown meeting')
                
                alert = {
                    "type": "meeting_reminder", 
                    "title": f"Upcoming: {title}",
                    "message": "You have this meeting scheduled",
                    "priority": "medium"
                }
                alerts.append(alert)
        
        return alerts

    def _calculate_meeting_importance(self, event: Dict) -> float:
        """Calculate importance of a meeting based on various factors"""
        importance = 0.5  # Base importance
        
        # Factor 1: Number of attendees
        attendees = event.get('attendees', [])
        if len(attendees) > 5:
            importance += 0.2
        elif len(attendees) > 10:
            importance += 0.3
        
        # Factor 2: Keywords in title
        title = event.get('summary', '').lower()
        important_keywords = ['review', 'important', 'urgent', 'executive', 'client']
        if any(keyword in title for keyword in important_keywords):
            importance += 0.2
        
        # Factor 3: Video conference
        if event.get('hangoutLink'):
            importance += 0.1
        
        return min(importance, 1.0)