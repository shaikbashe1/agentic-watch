import httpx
from typing import Dict, Any
import agentwatch

class PolicyViolationError(Exception):
    """Raised when the AgentWatch policy engine blocks an action."""
    pass

class AgentWatchGuard:
    """
    Acts as a synchronous guard rail before an agent executes a sensitive action
    (e.g., executing a tool, sending a prompt).
    """
    
    @classmethod
    def evaluate_action(cls, event_type: str, payload: Dict[str, Any]):
        if not agentwatch._config.policy_enforcement:
            return # Enforcement is disabled, allow everything
            
        try:
            # We use a synchronous request here because we MUST block the main thread
            # before the action happens. This is the difference between passive telemetry
            # and active governance.
            
            client = httpx.Client(base_url="http://localhost:8000/api/v1", timeout=2.0)
            headers = {"Authorization": f"Bearer {agentwatch._config.api_key}"}
            
            req_data = {
                "workspace_id": agentwatch._config.workspace_id,
                "agent_name": agentwatch._config.agent_name,
                "event_type": event_type,
                "payload": payload
            }
            
            response = client.post("/governance/evaluate", json=req_data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                decision = result.get("decision", "allow")
                
                if decision == "block":
                    raise PolicyViolationError(f"Action blocked by AgentWatch Policy Engine: {result.get('reason')}")
                elif decision == "warn":
                    print(f"[AgentWatch WARN] {result.get('reason')} (Risk Score: {result.get('risk_score')})")
                    
        except httpx.RequestError:
            # If the governance engine is unreachable, we typically fail-open in production
            # to avoid bringing down the user's application, but we log the outage.
            print("[AgentWatch] Warning: Governance API unreachable. Failing open.")
