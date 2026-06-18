export class AgentWatch {
    private apiKey: string;
    private apiUrl: string;

    constructor(apiKey?: string, apiUrl?: string) {
        this.apiKey = apiKey || process.env.AGENTWATCH_API_KEY || '';
        this.apiUrl = apiUrl || process.env.AGENTWATCH_API_URL || 'http://localhost:8000';

        if (!this.apiKey) {
            console.warn("AgentWatch initialized without an API Key.");
        }
    }

    public async track(payload: {
        event_type: string;
        agent_id: string;
        [key: string]: any;
    }): Promise<void> {
        try {
            await fetch(`${this.apiUrl}/telemetry`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-API-Key': this.apiKey
                },
                body: JSON.stringify({
                    timestamp: Date.now(),
                    ...payload
                })
            });
        } catch (error) {
            // Fail silently so we don't crash the main process
        }
    }
}
