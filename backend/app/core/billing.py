from dataclasses import dataclass
from typing import Optional

@dataclass
class Plan:
    events_per_month: int # -1 for unlimited
    agents: int # -1 for unlimited
    retention_days: int
    policies: int # -1 for unlimited
    team_members: int # -1 for unlimited
    price_usd: str | int
    sso: bool = False
    saml: bool = False
    soc2_reports: bool = False
    dedicated_support: bool = False

class PricingPlan:
    FREE = Plan(
        events_per_month=10_000,
        agents=3,
        retention_days=7,
        policies=5,
        team_members=1,
        price_usd=0
    )
    
    STARTER = Plan(
        events_per_month=500_000,
        agents=10,
        retention_days=30,
        policies=50,
        team_members=5,
        price_usd=49
    )
    
    GROWTH = Plan(
        events_per_month=5_000_000,
        agents=50,
        retention_days=90,
        policies=-1,
        team_members=25,
        price_usd=299
    )
    
    ENTERPRISE = Plan(
        events_per_month=-1,
        agents=-1,
        retention_days=730,
        policies=-1,
        team_members=-1,
        sso=True,
        saml=True,
        soc2_reports=True,
        dedicated_support=True,
        price_usd="custom"
    )

class UsageMeter:
    def __init__(self, plan: Plan):
        self.plan = plan
        self.events_ingested = 0
        self.agents_monitored = 0
        self.policies_evaluated = 0
        self.data_retained_gb = 0.0
        self.api_calls_made = 0

    def record_event(self) -> bool:
        """Record an event and return True if within plan limits."""
        if self.plan.events_per_month != -1 and self.events_ingested >= self.plan.events_per_month:
            return False
        self.events_ingested += 1
        return True

    def register_agent(self) -> bool:
        if self.plan.agents != -1 and self.agents_monitored >= self.plan.agents:
            return False
        self.agents_monitored += 1
        return True
