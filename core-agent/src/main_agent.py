import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import sys
import os

# Add the core-agent src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from context_engine.engine import ContextEngine
from memory.vector_store import VectorMemory

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProactiveAIAgent:
    def __init__(self):
        self.vector_memory = VectorMemory()
        self.context_engine = ContextEngine(self.vector_memory)
        self.is_running = False
        self.last_poll_time = datetime.now()
    
    async def initialize(self):
        """Initialize the AI agent with real data sources"""
        logger.info("🚀 Initializing Proactive AI Agent...")
        
        try:
            # Try to initialize with real calendar data
            await self._initialize_real_calendar()
            logger.info("✅ Real calendar integration initialized")
        except Exception as e:
            logger.warning(f"⚠️  Real calendar not available, using demo data: {e}")
            await self._initialize_demo_data()
        
        logger.info("✅ AI Agent initialized successfully!")
    
    async def _initialize_real_calendar(self):
        """Initialize with real Google Calendar data"""
        try:
            # Add the mcp-servers directory to path
            mcp_path = os.path.join(os.path.dirname(__file__), '..', '..', 'mcp-servers', 'calendar')
            sys.path.append(mcp_path)
            
            from google_calendar_server import GoogleCalendarServer
            
            calendar_server = GoogleCalendarServer()
            events = await calendar_server.get_upcoming_events(20)  # Next 20 events
            
            if events:
                await self.context_engine.update_context("calendar", events)
                logger.info(f"📅 Loaded {len(events)} calendar events")
            else:
                logger.warning("No calendar events found")
                await self._initialize_demo_data()
                
        except ImportError as e:
            logger.warning(f"Google Calendar not set up: {e}")
            await self._initialize_demo_data()
        except Exception as e:
            logger.warning(f"Error loading calendar: {e}")
            await self._initialize_demo_data()
    
    async def _initialize_demo_data(self):
        """Initialize with demo data if real sources aren't available"""
        demo_data = {
            "source": "demo",
            "events": [
                {
                    "id": "1",
                    "summary": "Team Standup Meeting",
                    "start": {"dateTime": "2024-01-15T10:00:00Z"},
                    "end": {"dateTime": "2024-01-15T10:30:00Z"},
                    "description": "Daily team synchronization",
                    "attendees": [{"email": "team@company.com"}]
                },
                {
                    "id": "2", 
                    "summary": "Project Phoenix Review",
                    "start": {"dateTime": "2024-01-15T14:00:00Z"},
                    "end": {"dateTime": "2024-01-15T15:30:00Z"},
                    "description": "Quarterly project review with stakeholders",
                    "attendees": [{"email": "stakeholders@company.com"}]
                }
            ]
        }
        
        await self.context_engine.update_context("demo", demo_data)
        logger.info("📋 Loaded demo calendar data")
    
    async def run_continuous_agent(self):
        """Run the continuous monitoring agent"""
        self.is_running = True
        logger.info("🔄 Starting continuous monitoring...")
        logger.info("   This will check your calendar and provide proactive alerts every 30 seconds")
        logger.info("   Press Ctrl+C to stop monitoring")
        
        iteration = 0
        try:
            while self.is_running:
                iteration += 1
                print(f"\n--- Monitoring Cycle {iteration} ---")
                
                # Check for proactive alerts
                await self._check_proactive_alerts()
                
                # Perform proactive context analysis
                await self._proactive_context_analysis()
                
                # Update last poll time
                self.last_poll_time = datetime.now()
                
                # Wait before next iteration
                await asyncio.sleep(30)
                
        except KeyboardInterrupt:
            logger.info("🛑 Shutting down agent...")
            self.is_running = False
        except Exception as e:
            logger.error(f"❌ Error in main loop: {e}")
            self.is_running = False
    
    async def _check_proactive_alerts(self):
        """Check for and display proactive alerts"""
        try:
            # Get upcoming meetings in next 24 hours
            upcoming = await self.context_engine.get_relevant_context("meeting today tomorrow", 10)
            
            current_time = datetime.now()
            alerts = []
            
            for item in upcoming:
                metadata = item.get('metadata', {})
                if metadata.get('type') == 'meeting':
                    # Simple time-based alert logic
                    content_str = item.get('document', '')
                    if 'start_time' in content_str:
                        # Extract time and check if it's within next 2 hours
                        # For MVP, we'll create alerts for all upcoming meetings
                        title = metadata.get('content', {}).get('title', 'Unknown meeting')
                        
                        alert = {
                            "type": "MEETING_REMINDER",
                            "title": f"Upcoming: {title}",
                            "message": f"You have this meeting coming up",
                            "priority": "MEDIUM",
                            "suggestions": ["Review meeting details", "Prepare any materials"]
                        }
                        alerts.append(alert)
            
            # Display alerts
            if alerts:
                print("🚨 PROACTIVE ALERTS:")
                for alert in alerts:
                    print(f"   📢 {alert['title']}")
                    print(f"   💬 {alert['message']}")
                    print(f"   ⚡ {alert['suggestions'][0]}")
                    print()
            else:
                print("✅ No urgent alerts at this time")
                
        except Exception as e:
            logger.error(f"Error checking alerts: {e}")
    
    async def _proactive_context_analysis(self):
        """Perform proactive analysis of current context"""
        try:
            # Analyze upcoming meetings
            upcoming = await self.context_engine.get_relevant_context("meeting today", 5)
            if upcoming:
                print(f"📊 Context Analysis: {len(upcoming)} upcoming meetings today")
                for item in upcoming[:3]:  # Show first 3
                    doc = item.get('document', '')
                    # Extract meeting title from document
                    if "meeting: " in doc:
                        title = doc.split("meeting: ")[1].split(",")[0]
                        print(f"   • {title}")
            
            # Look for birthday/anniversary alerts
            celebrations = await self.context_engine.get_relevant_context("birthday anniversary", 3)
            if celebrations:
                print(f"🎉 Upcoming celebrations: {len(celebrations)}")
                for item in celebrations[:2]:
                    doc = item.get('document', '')
                    if "birthday" in doc.lower() or "anniversary" in doc.lower():
                        print(f"   • {doc[:60]}...")
                        
        except Exception as e:
            logger.error(f"Error in context analysis: {e}")
    
    async def interactive_search(self):
        """Allow interactive context searching"""
        print("\n🔍 INTERACTIVE CONTEXT SEARCH")
        print("   Search through your calendar events and context")
        print("   Type 'quit' to return to main menu")
        
        while True:
            try:
                query = input("\n🔎 Enter search query: ").strip()
                if query.lower() in ['quit', 'exit', 'q']:
                    break
                
                if query:
                    print(f"   Searching for: '{query}'")
                    results = await self.context_engine.get_relevant_context(query, 5)
                    
                    if results:
                        print(f"   📖 Found {len(results)} results:")
                        for i, result in enumerate(results, 1):
                            doc = result.get('document', 'No content')
                            # Clean up the display
                            if len(doc) > 120:
                                doc = doc[:120] + "..."
                            print(f"   {i}. {doc}")
                    else:
                        print("   ❌ No results found")
                        
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Search error: {e}")
    
    async def check_current_context(self):
        """Display current context summary"""
        print("\n📋 CURRENT CONTEXT SUMMARY")
        print("=" * 40)
        
        try:
            # Get recent meetings
            recent = await self.context_engine.get_relevant_context("meeting", 10)
            if recent:
                print(f"📅 Recent/Upcoming Events: {len(recent)}")
                for item in recent[:5]:
                    doc = item.get('document', '')
                    if "meeting: " in doc:
                        # Extract clean title
                        title_part = doc.split("meeting: ")[1]
                        title = title_part.split(",")[0] if "," in title_part else title_part
                        print(f"   • {title}")
            
            # Get personal events
            personal = await self.context_engine.get_relevant_context("birthday anniversary", 5)
            if personal:
                print(f"\n🎊 Personal Events: {len(personal)}")
                for item in personal[:3]:
                    doc = item.get('document', '')
                    print(f"   • {doc[:80]}...")
                    
        except Exception as e:
            logger.error(f"Error getting context: {e}")

# For direct execution
async def main():
    """Main entry point when run directly"""
    ai_agent = ProactiveAIAgent()
    
    print("🤖 Proactive Context-Awareness AI Agent")
    print("=" * 50)
    
    await ai_agent.initialize()
    
    while True:
        print("\nOptions:")
        print("1. Run continuous monitoring")
        print("2. Interactive context search") 
        print("3. Check current context")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            await ai_agent.run_continuous_agent()
        elif choice == "2":
            await ai_agent.interactive_search()
        elif choice == "3":
            await ai_agent.check_current_context()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    asyncio.run(main())