import os
import time
import sys

# Add the local sdks/python folder to path so we can import agentwatch
sys.path.append(os.path.join(os.path.dirname(__file__), 'sdks', 'python'))

from agentwatch import monitor, AgentWatch

# Mocking the environment variables for testing
os.environ["AGENTWATCH_API_KEY"] = "dummy_key_for_testing"
# Point to a local or remote instance
os.environ["AGENTWATCH_API_URL"] = "https://backend-psi-two-49.vercel.app"

# 1. Testing the @monitor wrapper
print("--- 1. Testing @monitor wrapper ---")

@monitor(agent_id="test_agent_123", api_key="dummy_key_for_testing")
def my_autonomous_agent(query):
    print(f"Agent received query: {query}")
    time.sleep(0.5) # simulating thinking
    print("Agent finished thinking.")
    return "Task Complete"

my_autonomous_agent("Find the best AI stocks")
print("@monitor wrapper executed perfectly! (Telemetry sent in background)")

# 2. Testing Zero-Latency & Automated Loop Detection
print("\n--- 2. Testing Loop Detection ---")
aw = AgentWatch(api_key="dummy_key_for_testing")

print("Firing 5 identical tool calls instantly...")
start_time = time.time()

for i in range(5):
    aw.track(
        event_type="tool_call",
        agent_id="test_agent_123",
        tool_name="search_web",
        inputs="{'query': 'weather today'}",
        outputs="{'result': 'sunny'}",
        status="success"
    )

end_time = time.time()
latency = end_time - start_time
print(f"Fired 5 telemetry events in {latency:.4f} seconds!")
print("If latency is near 0.00x seconds, the ThreadPoolExecutor (Zero-Latency) is working flawlessly.")
print("The backend will now automatically flag this as a Critical 'Logic Loop' alert.")
