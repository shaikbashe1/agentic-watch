from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Agentic Watch - Enterprise Integration Guide', 0, 1, 'C')
        self.ln(5)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, body)
        self.ln(5)

pdf = PDF()
pdf.add_page()

pdf.chapter_title('1. Account & Workspace Setup')
pdf.chapter_body('Navigate to the Agentic Watch platform to create your enterprise account. Once registered, create a dedicated Workspace for your company. Use Role-Based Access Control (RBAC) to invite team members as Developers, Admins, or Viewers based on their responsibilities.')

pdf.chapter_title('2. Registering Your AI Agents')
pdf.chapter_body('Within your Workspace, navigate to the Agent Connection Wizard. Register each internal AI agent separately. You will need to specify the Agent Name and its underlying Framework (e.g., LangGraph, CrewAI, AutoGen). This logical separation allows for granular governance across different departments.')

pdf.chapter_title('3. API Key Generation')
pdf.chapter_body('Upon registering an agent, the platform will automatically provision a unique, cryptographically secure API Key for that specific agent. This key is used to authenticate telemetry payloads. Keep this key secure and inject it into your agent environments via secure secret managers (e.g., AWS Secrets Manager, HashiCorp Vault).')

pdf.chapter_title('4. Installing the AgentWatch SDK')
pdf.chapter_body('Agentic Watch operates as an out-of-band telemetry engine. Install the lightweight SDK into your agent\'s environment:\n\nFor Python environments:\n$ pip install agentwatch\n\nFor Node.js environments:\n$ npm install agentwatch')

pdf.chapter_title('5. Integrating Telemetry Tracking')
pdf.chapter_body('Import the SDK and initialize the AgentWatch client using the generated API Key. Insert the tracking method into your agent\'s execution loop to push events to the platform.\n\nExample (Python):\nfrom agentwatch import AgentWatch\naw = AgentWatch(api_key="YOUR_API_KEY")\n\naw.track(\n    event_type="tool_call",\n    agent_id="YOUR_AGENT_ID",\n    tool_name="DatabaseQuery",\n    status="success",\n    latency=150\n)')

pdf.chapter_title('6. Live Monitoring & Governance')
pdf.chapter_body('Once the first telemetry packet is securely received, your agent\'s status will change to "Connected" on the dashboard. You can now monitor real-time Execution Timelines, Tool Traces, Token Costs, and Goal Alignment metrics directly from the Agentic Watch portal. Configure Custom Policies to automatically alert your security team if anomalous agent behavior is detected.')

output_path = r'C:\Users\dell\.gemini\antigravity\brain\041ca41a-e000-4b6f-a27a-96f9a61c36a2\Agentic_Watch_Integration_Guide.pdf'
pdf.output(output_path)
print(f"PDF generated successfully at {output_path}")
