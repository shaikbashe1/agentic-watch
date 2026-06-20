import os
import sys
import time
import uuid
import httpx

# Ensure we use the local sdk if not installed via pip
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sdks', 'python'))
import agentwatch

API_BASE = "https://backend-psi-two-49.vercel.app"

def setup_account():
    # 1. Register a test user
    email = f"test_{uuid.uuid4().hex[:6]}@example.com"
    print(f"[*] Registering test account: {email}")
    
    res = httpx.post(f"{API_BASE}/auth/register", json={
        "workspace_name": "Test Workspace",
        "email": email,
        "password": "password123"
    })
    
    if res.status_code != 200:
        print(f"Error registering: {res.text}")
        sys.exit(1)
        
    token = res.json()["access_token"]
    
    # 2. Generate API Key
    print("[*] Generating AgentWatch API Key...")
    res_key = httpx.post(f"{API_BASE}/api-keys", json={
        "name": "Live Test Key"
    }, headers={"Authorization": f"Bearer {token}"})
    
    if res_key.status_code != 200:
        print(f"Error generating key: {res_key.text}")
        sys.exit(1)
        
    api_key = res_key.json()["key"]
    print(f"[+] Successfully generated API Key: {api_key[:15]}...")
    
    return api_key

if __name__ == "__main__":
    print("==============================================")
    print(" AgentWatch Live End-to-End Test")
    print("==============================================")
    
    api_key = setup_account()
    
    print("\n[*] Initializing AgentWatch SDK...")
    agentwatch.init(api_key=api_key, api_url=API_BASE, environment="production")
    client = agentwatch.get_client()
    
    print("\n[*] Running manual test agent (simulating an LLM tool call)...")
    
    print(f"[Agent] Calling tool: 'search_web'")
    
    # Simulate an intercepted tool call event
    client.send_event({
        "event_type": "tool_call",
        "agent_id": "live_demo_agent",
        "tool_name": "search_web",
        "inputs": {"query": "Quantum Computing"},
        "outputs": {"result": "Found 100 articles on Quantum Computing"},
        "status": "success",
        "latency": 0.5,
        "cost": 0.001
    })
    
    print("[Agent] Analyzing results...")
    time.sleep(1)
    
    print("[Agent] Formatting response...")
    
    # Wait a second for background telemetry thread to flush
    time.sleep(2)
    print("\n[+] Success! All telemetry sent to the live Vercel backend.")
    print("    You can log in to the dashboard with the generated credentials to view the traces!")
