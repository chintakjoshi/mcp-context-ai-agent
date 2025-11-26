import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Vector database
    CHROMA_PERSIST_DIR = "./data/chroma"
    
    # MCP Server URLs (we'll use mock data first)
    MCP_CALENDAR_URL = "mock://calendar"
    MCP_GMAIL_URL = "mock://gmail"
    
    # AI/ML settings
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    
settings = Settings()