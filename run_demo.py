#!/usr/bin/env python3
"""
Simple demo runner for Proactive Context-Awareness AI
"""
import sys
import os

# Add the core-agent to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core-agent', 'src'))

async def main():
    try:
        from main_agent import ProactiveAIAgent
        
        print("🚀 Starting Proactive Context-Awareness AI Agent")
        print("=" * 50)
        
        ai_agent = ProactiveAIAgent()
        await ai_agent.initialize()
        
        # Show the menu instead of calling non-existent main()
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
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please make sure all files are in the correct locations.")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())