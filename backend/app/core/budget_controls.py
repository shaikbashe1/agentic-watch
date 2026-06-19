from typing import List, Dict, Optional
import logging

class BudgetControl:
    def __init__(
        self,
        workspace_id: str,
        monthly_budget_usd: float,
        alert_at_percent: List[int] = [50, 80, 95, 100],
        action_at_100_percent: str = "warn", # or "block"
        per_agent_budget: Dict[str, float] = None,
        per_session_limit: float = None
    ):
        self.workspace_id = workspace_id
        self.monthly_budget_usd = monthly_budget_usd
        self.alert_at_percent = alert_at_percent
        self.action_at_100_percent = action_at_100_percent
        self.per_agent_budget = per_agent_budget or {}
        self.per_session_limit = per_session_limit

    def check_budget(self, agent_id: str, current_spend: float, session_spend: float, new_cost: float) -> str:
        """
        Check if adding new_cost exceeds any budgets.
        Returns "ALLOW", "WARN", or "BLOCK"
        """
        projected_total = current_spend + new_cost
        
        # Check session limit
        if self.per_session_limit is not None and (session_spend + new_cost) > self.per_session_limit:
            logging.warning(f"Session limit exceeded for agent {agent_id}. Limit: {self.per_session_limit}")
            return "BLOCK"

        # Check agent-specific limit
        agent_budget = self.per_agent_budget.get(agent_id)
        if agent_budget is not None and projected_total > agent_budget:
            logging.warning(f"Agent budget exceeded for agent {agent_id}. Limit: {agent_budget}")
            return "BLOCK"

        # Check overall workspace budget
        if projected_total > self.monthly_budget_usd:
            logging.warning(f"Workspace budget exceeded. Limit: {self.monthly_budget_usd}")
            return self.action_at_100_percent.upper()

        return "ALLOW"
