from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum

class ContextType(Enum):
    MEETING = "meeting"
    PROJECT = "project" 
    TASK = "task"
    COMMUNICATION = "communication"
    HEALTH = "health"

@dataclass
class ContextEntity:
    id: str
    type: str
    content: Dict[str, Any]
    timestamp: datetime
    importance: float
    relationships: List[str]