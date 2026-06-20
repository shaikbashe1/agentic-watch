import logging
from typing import List, Any
import requests

class AlertDecision:
    def __init__(self, triggered: bool, rule_name: str, severity: str, channels: List[str], payload: dict):
        self.triggered = triggered
        self.rule_name = rule_name
        self.severity = severity
        self.channels = channels
        self.payload = payload

class AlertEngine:
    def evaluate(self, alert_rules: List[Any], event_data: dict) -> List[AlertDecision]:
        decisions = []
        
        for rule in alert_rules:
            if not getattr(rule, "enabled", True) and not rule.get("enabled", True):
                continue
                
            condition = getattr(rule, "condition", {})
            if isinstance(rule, dict):
                condition = rule.get("condition", {})
                
            if not condition:
                continue
                
            metric = condition.get("metric")
            operator = condition.get("operator")
            threshold = condition.get("threshold")
            
            # Simple synchronous event evaluation for now
            # (In production, threshold alerts over time windows require TSDB aggregations)
            if metric == "risk_score":
                actual = event_data.get("risk_score", 0)
                if self._evaluate_condition(actual, operator, threshold):
                    decisions.append(self._trigger(rule, event_data))
                    
            elif metric == "latency":
                actual = event_data.get("latency_ms", 0)
                if self._evaluate_condition(actual, operator, threshold):
                    decisions.append(self._trigger(rule, event_data))
                    
        return decisions
        
    def _trigger(self, rule: Any, event_data: dict) -> AlertDecision:
        name = getattr(rule, "name", "Unnamed Rule") if not isinstance(rule, dict) else rule.get("name", "Unnamed")
        severity = getattr(rule, "severity", "warning") if not isinstance(rule, dict) else rule.get("severity", "warning")
        channels = getattr(rule, "channels", []) if not isinstance(rule, dict) else rule.get("channels", [])
        
        return AlertDecision(
            triggered=True,
            rule_name=name,
            severity=severity,
            channels=channels,
            payload=event_data
        )

    def dispatch(self, decision: AlertDecision):
        if not decision.triggered:
            return
            
        logging.info(f"ALERT FIRED: {decision.rule_name} [{decision.severity}]")
        
        for channel in decision.channels:
            if channel.startswith("http"):
                try:
                    requests.post(channel, json={
                        "alert": decision.rule_name,
                        "severity": decision.severity,
                        "event": decision.payload
                    }, timeout=2)
                except Exception as e:
                    logging.error(f"Failed to dispatch webhook alert: {e}")
            elif channel.startswith("slack:"):
                # Handle slack webhook
                pass
            
    def _evaluate_condition(self, actual_value: Any, operator: str, expected_value: Any) -> bool:
        if actual_value is None:
            return False
            
        try:
            if operator == "gt":
                return float(actual_value) > float(expected_value)
            elif operator == "lt":
                return float(actual_value) < float(expected_value)
            elif operator == "eq":
                return float(actual_value) == float(expected_value)
            return False
        except (ValueError, TypeError):
            return False
