import asyncio
from typing import Dict, List
import logging
from datetime import datetime, timedelta
from context_engine.engine import ContextEngine
from alert_system.triage import AlertTriage, Alert, AlertType, AlertPriority
from memory.vector_store import VectorMemory

class ProactiveAIAgent:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.vector_memory = VectorMemory()
        self.context_engine = ContextEngine(self.vector_memory, None)  # Add LLM client
        self.alert_triage = AlertTriage()
        
        # MCP clients
        self.mcp_clients: Dict[str, Any] = {}
        
        # State
        self.is_running = False
    
    async def initialize(self):
        """Initialize MCP connections and components"""
        await self._initialize_mcp_clients()
        await self._load_historical_context()
        
        self.logger.info("Proactive AI Agent initialized")
    
    async def run_continuous_loop(self):
        """Main agent loop"""
        self.is_running = True
        
        while self.is_running:
            try:
                # Poll MCP servers for updates
                await self._poll_data_sources()
                
                # Process any pending alerts
                await self._process_pending_alerts()
                
                # Run periodic context analysis
                await self._periodic_context_analysis()
                
                await asyncio.sleep(30)  # Poll every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                await asyncio.sleep(60)  # Back off on error
    
    async def _poll_data_sources(self):
        """Poll all MCP servers for new data"""
        polling_tasks = []
        
        for source, client in self.mcp_clients.items():
            task = asyncio.create_task(self._poll_single_source(source, client))
            polling_tasks.append(task)
        
        await asyncio.gather(*polling_tasks, return_exceptions=True)
    
    async def _poll_single_source(self, source: str, client):
        """Poll a single data source"""
        try:
            # Get updates since last poll
            updates = await client.get_updates(since=self.last_poll_time)
            
            if updates:
                await self.context_engine.update_context(source, updates)
                self.logger.info(f"Processed {len(updates)} updates from {source}")
                
        except Exception as e:
            self.logger.error(f"Error polling {source}: {e}")
    
    async def _process_pending_alerts(self):
        """Process and deliver validated alerts"""
        # This would integrate with your notification system
        # For now, just log
        pending_alerts = await self._generate_alerts()
        
        for alert in pending_alerts:
            if await self.alert_triage.evaluate_alert(alert):
                await self._deliver_alert(alert)
    
    async def _generate_alerts(self) -> List[Alert]:
        """Generate potential alerts based on current context"""
        alerts = []
        
        # Meeting preparation alerts
        alerts.extend(await self._check_meeting_prep())
        
        # Project consistency alerts
        alerts.extend(await self._check_project_consistency())
        
        # Health and wellness alerts
        alerts.extend(await self._check_wellness())
        
        return alerts
    
    async def _check_meeting_prep(self) -> List[Alert]:
        """Generate meeting preparation alerts"""
        alerts = []
        
        # Get upcoming meetings in next 2 hours
        upcoming_meetings = await self._get_upcoming_meetings(hours_ahead=2)
        
        for meeting in upcoming_meetings:
            # Check if user has relevant documents open/unsaved
            # Check recent communications about this meeting
            # Check if meeting requires preparation
            
            alert = Alert(
                id=f"meeting_prep_{meeting['id']}",
                type=AlertType.MEETING_REMINDER,
                priority=AlertPriority.MEDIUM,
                message=f"Meeting with {meeting['title']} in 30 minutes. You have unsaved documents related to this meeting.",
                context=meeting,
                confidence=0.8,
                suggested_actions=["Open related documents", "Review meeting notes"]
            )
            alerts.append(alert)
        
        return alerts
    
    async def _deliver_alert(self, alert: Alert):
        """Deliver alert to user (integrate with your frontend)"""
        self.logger.info(f"ALERT: {alert.message}")
        
        # Here you would integrate with:
        # - Desktop notifications
        # - Mobile app push notifications  
        # - Web interface
        # - Email summary digests
        
        # For now, just print
        print(f"\n🚨 PROACTIVE ALERT: {alert.message}")
        print(f"   Suggested: {', '.join(alert.suggested_actions)}")