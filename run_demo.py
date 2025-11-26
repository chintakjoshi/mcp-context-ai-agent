#!/usr/bin/env python3
"""
Simple demo runner for Proactive Context-Awareness AI
"""
import sys
import os

# Add the core-agent to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core-agent', 'src'))

async def main():
    from main_agent import SimpleProactiveAI
    
    print("🚀 Starting Proactive Context-Awareness AI Demo")
    print("=" * 50)
    
    ai_agent = SimpleProactiveAI()
    await ai_agent.initialize()
    await ai_agent.run_demo()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())