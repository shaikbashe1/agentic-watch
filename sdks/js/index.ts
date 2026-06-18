export const monitor = (agent: any) => {
    const API_URL = process.env.AGENTWATCH_API_URL || 'http://localhost:8000';
    const API_KEY = process.env.AGENTWATCH_API_KEY || '';
    
    return new Proxy(agent, {
        get(target, prop, receiver) {
            const originalValue = Reflect.get(target, prop, receiver);
            
            if (typeof originalValue === 'function' && prop === 'run') {
                return async function(...args: any[]) {
                    const agentId = target.id || 'default_agent';
                    const startTime = Date.now();
                    
                    fetch(`${API_URL}/telemetry`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json', 'X-API-Key': API_KEY },
                        body: JSON.stringify({
                            event_type: 'timeline_step',
                            agent_id: agentId,
                            step_type: 'Planning',
                            status: 'Started',
                            duration_ms: 0
                        })
                    }).catch(console.error);

                    try {
                        const result = await originalValue.apply(this, args);
                        const duration = Date.now() - startTime;
                        
                        fetch(`${API_URL}/telemetry`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json', 'X-API-Key': API_KEY },
                            body: JSON.stringify({
                                event_type: 'timeline_step',
                                agent_id: agentId,
                                step_type: 'Final Output',
                                status: 'Success',
                                duration_ms: duration
                            })
                        }).catch(console.error);
                        
                        return result;
                    } catch (error) {
                        const duration = Date.now() - startTime;
                        
                        fetch(`${API_URL}/telemetry`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json', 'X-API-Key': API_KEY },
                            body: JSON.stringify({
                                event_type: 'timeline_step',
                                agent_id: agentId,
                                step_type: 'Final Output',
                                status: 'Failed',
                                duration_ms: duration
                            })
                        }).catch(console.error);
                        
                        throw error;
                    }
                };
            }
            
            return originalValue;
        }
    });
};
