class LocalRiskScorer:
    def __init__(self):
        # Basic offline heuristics
        self.dangerous_keywords = ["rm -rf", "drop table", "delete from", "truncate", "systemctl stop"]
        
    def score_event(self, event_data: dict) -> int:
        score = 0
        payload = str(event_data.get("payload", ""))
        
        for kw in self.dangerous_keywords:
            if kw in payload.lower():
                score += 50
                
        if event_data.get("event_type") == "error":
            score += 20
            
        return min(score, 100)
