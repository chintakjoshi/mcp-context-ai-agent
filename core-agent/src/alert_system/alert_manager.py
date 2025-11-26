from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
import logging
from dataclasses import dataclass
from enum import Enum

class AlertPriority(Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRITICAL = "critical"

class AlertType(Enum):
    MEETING_REMINDER = "meeting_reminder"
    MEETING_PREP = "meeting_preparation"
    SCHEDULE_CONFLICT = "schedule_conflict"
    FOLLOW_UP = "follow_up"
    HEALTH = "health_advice"

@dataclass
class Alert:
    id: str
    type: AlertType
    priority: AlertPriority
    title: str
    message: str
    context: Dict[str, Any]
    timestamp: datetime
    suggested_actions: List[str]
    confidence: float = 0.8

class AlertManager:
    def __init__(self, context_engine):
        self.context_engine = context_engine
        self.logger = logging.getLogger(__name__)
        self.alert_history: List[Alert] = []
        
    async def check_for_alerts(self) -> List[Alert]:
        """Check all alert conditions and return active alerts"""
        alerts = []
        
        # Check meeting alerts
        alerts.extend(await self._check_meeting_alerts())
        
        # Check schedule conflicts
        alerts.extend(await self._check_schedule_conflicts())
        
        # Check follow-up needs
        alerts.extend(await self._check_follow_ups())
        
        # Update alert history
        self.alert_history.extend(alerts)
        
        return alerts
    
    async def _check_meeting_alerts(self) -> List[Alert]:
        """Check for meeting-related alerts"""
        alerts = []
        
        # Get upcoming meetings in next 2 hours
        upcoming_context = await self.context_engine.get_relevant_context("meeting today", 10)
        
        for context_item in upcoming_context:
            metadata = context_item.get('metadata', {})
            if metadata.get('type') != 'meeting':
                continue
                
            content_str = context_item.get('document', '{}')
            # Parse the content (simplified - in real implementation, store properly)
            if 'start_time' in content_str:
                # Extract time logic would go here
                # For now, create sample alerts
                
                alert = Alert(
                    id=f"meeting_{len(alerts)}",
                    type=AlertType.MEETING_PREP,
                    priority=AlertPriority.MEDIUM,
                    title="Upcoming Meeting",
                    message=f"You have a meeting soon: {metadata.get('content', {}).get('title', 'Unknown')}",
                    context=metadata,
                    timestamp=datetime.now(),
                    suggested_actions=[
                        "Review meeting agenda",
                        "Prepare documents",
                        "Join meeting room"
                    ]
                )
                alerts.append(alert)
        
        return alerts
    
    async def _check_schedule_conflicts(self) -> List[Alert]:
        """Check for scheduling conflicts"""
        # This would analyze calendar for overlapping events, back-to-back meetings, etc.
        alerts = []
        
        # Sample conflict detection
        conflict_alert = Alert(
            id="conflict_1",
            type=AlertType.SCHEDULE_CONFLICT,
            priority=AlertPriority.HIGH,
            title="Potential Schedule Conflict",
            message="You have back-to-back meetings from 2-4 PM today",
            context={"time_range": "14:00-16:00"},
            timestamp=datetime.now(),
            suggested_actions=[
                "Consider adding buffer time",
                "Prepare quick transition",
                "Inform attendees if needed"
            ]
        )
        alerts.append(conflict_alert)
        
        return alerts
    
    async def _check_follow_ups(self) -> List[Alert]:
        """Check for follow-up actions needed"""
        alerts = []
        
        # Sample follow-up alert
        followup_alert = Alert(
            id="followup_1",
            type=AlertType.FOLLOW_UP,
            priority=AlertPriority.LOW,
            title="Follow-up Reminder",
            message="Consider following up on yesterday's client meeting",
            context={"meeting": "Client Review"},
            timestamp=datetime.now(),
            suggested_actions=[
                "Send summary email",
                "Schedule follow-up meeting",
                "Update project tracker"
            ]
        )
        alerts.append(followup_alert)
        
        return alerts
    
    def get_recent_alerts(self, hours: int = 24) -> List[Alert]:
        """Get alerts from the last specified hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [alert for alert in self.alert_history if alert.timestamp > cutoff]