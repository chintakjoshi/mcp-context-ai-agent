from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

class AlertPriority(Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRITICAL = "critical"

class AlertType(Enum):
    MEETING_REMINDER = "meeting_reminder"
    PROJECT_CONSISTENCY = "project_consistency"
    HEALTH_ADVICE = "health_advice"
    COMMUNICATION_PATTERN = "communication_pattern"

@dataclass
class Alert:
    id: str
    type: AlertType
    priority: AlertPriority
    message: str
    context: Dict[str, Any]
    confidence: float
    suggested_actions: List[str]

class AlertTriage:
    def __init__(self):
        self.alert_history = []
        self.feedback_history = []
        self.ml_model = RandomForestClassifier(n_estimators=100)
        self.is_trained = False
    
    async def evaluate_alert(self, alert: Alert) -> bool:
        """Determine if alert should be shown to user"""
        if not self.is_trained:
            # Initial rules-based approach
            return await self._rule_based_triage(alert)
        
        # ML-based approach
        features = self._extract_features(alert)
        prediction = self.ml_model.predict([features])[0]
        return prediction == 1
    
    async def _rule_based_triage(self, alert: Alert) -> bool:
        """Rule-based triage before ML model is trained"""
        base_rules = [
            # Time-based rules
            self._is_working_hours,
            # Priority threshold
            lambda a: a.priority in [AlertPriority.HIGH, AlertPriority.CRITICAL],
            # Context relevance
            self._has_high_context_relevance,
            # User activity state
            self._is_user_available
        ]
        
        score = sum(1 for rule in base_rules if rule(alert))
        return score >= 2
    
    def record_feedback(self, alert: Alert, was_useful: bool, user_feedback: str = ""):
        """Record user feedback for ML training"""
        self.feedback_history.append({
            "alert": alert,
            "was_useful": was_useful,
            "user_feedback": user_feedback,
            "timestamp": pd.Timestamp.now()
        })
        
        if len(self.feedback_history) >= 100:
            self._retrain_model()
    
    def _retrain_model(self):
        """Retrain ML model with new feedback"""
        if len(self.feedback_history) < 50:
            return
            
        # Prepare training data
        X = []
        y = []
        
        for feedback in self.feedback_history:
            features = self._extract_features(feedback["alert"])
            X.append(features)
            y.append(1 if feedback["was_useful"] else 0)
        
        # Train model
        self.ml_model.fit(X, y)
        self.is_trained = True
    
    def _extract_features(self, alert: Alert) -> List[float]:
        """Extract features for ML model"""
        return [
            alert.confidence,
            self._priority_to_numeric(alert.priority),
            len(alert.context),
            alert.context.get('urgency', 0),
            # Add more features based on context analysis
        ]
    
    def _priority_to_numeric(self, priority: AlertPriority) -> int:
        return {
            AlertPriority.LOW: 0,
            AlertPriority.MEDIUM: 1,
            AlertPriority.HIGH: 2,
            AlertPriority.CRITICAL: 3
        }[priority]