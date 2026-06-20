class Plan:
    def __init__(self, events_per_month, agents, retention_days, policies, team_members, price_usd):
        self.events_per_month = events_per_month
        self.agents = agents
        self.retention_days = retention_days
        self.policies = policies
        self.team_members = team_members
        self.price_usd = price_usd

class PricingPlan:
    FREE = Plan(events_per_month=10_000, agents=3, retention_days=7, policies=5, team_members=1, price_usd=0)
    STARTER = Plan(events_per_month=500_000, agents=10, retention_days=30, policies=50, team_members=5, price_usd=49)
    GROWTH = Plan(events_per_month=5_000_000, agents=50, retention_days=90, policies=-1, team_members=25, price_usd=299)
    ENTERPRISE = Plan(events_per_month=-1, agents=-1, retention_days=730, policies=-1, team_members=-1, price_usd="custom")

class UsageMeter:
    """
    Tracks telemetry ingestion usage against a workspace's pricing plan.
    """
    def __init__(self, workspace_id: str, plan: Plan):
        self.workspace_id = workspace_id
        self.plan = plan
        
    def check_ingestion_quota(self, current_events_this_month: int, batch_size: int = 1) -> bool:
        if self.plan.events_per_month == -1:
            return True # Unlimited
        
        if current_events_this_month + batch_size > self.plan.events_per_month:
            return False # Quota exceeded
            
        return True
