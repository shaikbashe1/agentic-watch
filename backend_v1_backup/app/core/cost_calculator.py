class CostCalculator:
    # Standard pricing in USD per 1 token (or 1M divided by 1,000,000)
    # Examples based on approx 2024 pricing
    MODEL_COSTS = {
        "gpt-4o": {"input": 0.000005, "output": 0.000015},
        "gpt-4-turbo": {"input": 0.00001, "output": 0.00003},
        "gpt-3.5-turbo": {"input": 0.0000005, "output": 0.0000015},
        "claude-3-5-sonnet": {"input": 0.000003, "output": 0.000015},
        "claude-3-opus": {"input": 0.000015, "output": 0.000075},
        "gemini-1.5-pro": {"input": 0.0000035, "output": 0.0000105},
        "gemini-1.5-flash": {"input": 0.00000035, "output": 0.00000105},
    }
    
    @classmethod
    def calculate_cost(cls, model: str, input_tokens: int, output_tokens: int) -> float:
        if not model:
            return 0.0
            
        # Try exact match
        cost_rates = cls.MODEL_COSTS.get(model.lower())
        
        # Try partial match if exact doesn't exist
        if not cost_rates:
            for known_model, rates in cls.MODEL_COSTS.items():
                if known_model in model.lower() or model.lower() in known_model:
                    cost_rates = rates
                    break
                    
        if not cost_rates:
            return 0.0
            
        return (input_tokens * cost_rates["input"]) + (output_tokens * cost_rates["output"])
