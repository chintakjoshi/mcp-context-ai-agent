import asyncio
import logging
from datetime import datetime
from context_engine.engine import ContextEngine
from memory.vector_store import VectorMemory

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleProactiveAI:
    def __init__(self):
        self.vector_memory = VectorMemory()
        self.context_engine = ContextEngine(self.vector_memory)
        self.is_running = False
    
    async def initialize(self):
        """Initialize the AI agent"""
        logger.info("Initializing Proactive AI Agent...")
        # Load any existing context
        await self._load_initial_data()
        logger.info("AI Agent initialized successfully!")
    
    async def _load_initial_data(self):
        """Load initial mock data for testing"""
        mock_data = {
            "source": "mock",
            "events": [
                {
                    "id": "1",
                    "summary": "Meeting with Acme Corp",
                    "start": {"dateTime": "2024-01-15T14:00:00Z"},
                    "end": {"dateTime": "2024-01-15T15:00:00Z"}
                }
            ]
        }
        await self.context_engine.update_context("mock", mock_data)
    
    async def run_demo(self):
        """Run a simple demo"""
        logger.info("Starting demo...")
        
        # Simulate receiving new data
        new_meeting = {
            "source": "mock",
            "events": [
                {
                    "id": "2", 
                    "summary": "Project Phoenix Kickoff",
                    "start": {"dateTime": "2024-01-16T10:00:00Z"},
                    "end": {"dateTime": "2024-01-16T11:00:00Z"}
                }
            ]
        }
        
        await self.context_engine.update_context("mock", new_meeting)
        
        # Search for relevant context
        results = await self.context_engine.get_relevant_context("project meeting")
        logger.info("Search results for 'project meeting':")
        for result in results:
            logger.info(f" - {result['document']}")
        
        # Keep running to simulate continuous operation
        logger.info("AI Agent is running... Press Ctrl+C to stop.")
        try:
            while True:
                await asyncio.sleep(10)
                # Simulate periodic context updates
                await self._simulate_data_update()
        except KeyboardInterrupt:
            logger.info("Shutting down...")
    
    async def _simulate_data_update(self):
        """Simulate receiving new data periodically"""
        # In a real implementation, this would poll MCP servers
        logger.info("Simulating data update...")
        
        # Add some random test data occasionally
        import random
        if random.random() < 0.3:  # 30% chance
            test_queries = ["urgent meeting", "project review", "team sync"]
            query = random.choice(test_queries)
            results = await self.context_engine.get_relevant_context(query, 2)
            logger.info(f"Proactive insight for '{query}': Found {len(results)} relevant items")

async def main():
    """Main entry point"""
    ai_agent = SimpleProactiveAI()
    await ai_agent.initialize()
    await ai_agent.run_demo()

if __name__ == "__main__":
    asyncio.run(main())