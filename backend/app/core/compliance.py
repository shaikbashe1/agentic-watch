class SOC2Report:
    """
    Generates compliance evidence reports for SOC2 audits.
    """
    
    def __init__(self, workspace_id: str, start_date: str, end_date: str):
        self.workspace_id = workspace_id
        self.start_date = start_date
        self.end_date = end_date
        
    def generate(self):
        return {
            "title": "SOC2 Compliance Report - AgentWatch",
            "period": f"{self.start_date} to {self.end_date}",
            "sections": {
                "access_control": "Evidence of RBAC and API key scopes...",
                "data_processing": "Logs of all agent telemetry processing...",
                "incident_log": "All policy violations that occurred in this window...",
                "change_management": "Audit trail of all policy/rule modifications...",
            }
        }

class RetentionPolicy:
    """
    Auto-deletes old data based on Workspace configuration.
    """
    def __init__(self, raw_events_days: int = 90, aggregated_metrics_days: int = 730):
        self.raw_events_days = raw_events_days
        self.aggregated_metrics_days = aggregated_metrics_days
        
    def apply(self, db_session):
        # In production, this would execute a DELETE query against TimescaleDB
        # e.g., DELETE FROM events WHERE started_at < NOW() - INTERVAL '90 days'
        pass
