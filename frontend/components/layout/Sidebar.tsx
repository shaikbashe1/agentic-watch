import Link from 'next/link';
import { LayoutDashboard, List, AlertTriangle, Shield, Target, Users, Webhook as WebhookIcon, Settings, LogOut } from 'lucide-react';

export function Sidebar() {
  return (
    <div className="w-64 border-r h-screen bg-card flex flex-col text-sm">
      <div className="p-6 font-bold text-lg flex items-center gap-2 border-b border-border">
        <Shield className="w-5 h-5 text-primary" /> AgentWatch
      </div>
      <div className="p-4 border-b border-border bg-muted/30">
        <div className="text-[10px] text-muted-foreground font-semibold mb-1 uppercase tracking-wider">Workspace</div>
        <select className="w-full bg-background border border-border p-1.5 rounded text-sm font-medium focus:ring-1 focus:ring-primary outline-none">
            <option>Acme Corp</option>
            <option>Personal Agents</option>
        </select>
      </div>
      <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
        <Link href="/" className="flex items-center gap-3 p-2 hover:bg-muted rounded-md font-medium text-foreground transition-colors">
          <LayoutDashboard className="w-4 h-4 text-muted-foreground" /> Dashboard
        </Link>
        <Link href="/activities" className="flex items-center gap-3 p-2 hover:bg-muted rounded-md font-medium text-muted-foreground hover:text-foreground transition-colors">
          <List className="w-4 h-4" /> Activity Logs
        </Link>
        <Link href="/alerts" className="flex items-center gap-3 p-2 hover:bg-muted rounded-md font-medium text-muted-foreground hover:text-foreground transition-colors">
          <AlertTriangle className="w-4 h-4" /> Alerts
        </Link>
        <Link href="/policies" className="flex items-center gap-3 p-2 hover:bg-muted rounded-md font-medium text-muted-foreground hover:text-foreground transition-colors">
          <Shield className="w-4 h-4 text-primary" /> Policies
        </Link>
        <Link href="/webhooks" className="flex items-center gap-3 p-2 hover:bg-muted rounded-md font-medium text-muted-foreground hover:text-foreground transition-colors">
          <WebhookIcon className="w-4 h-4 text-primary" /> Webhooks
        </Link>
        <Link href="/agents" className="flex items-center gap-3 p-2 hover:bg-muted rounded-md font-medium text-muted-foreground hover:text-foreground transition-colors">
          <Users className="w-4 h-4" /> Agents
        </Link>

        <div className="pt-6 pb-2 text-[10px] text-muted-foreground font-semibold uppercase tracking-wider">Observability</div>
        <Link href="/timeline" className="flex items-center gap-3 p-2 hover:bg-muted rounded-md font-medium text-muted-foreground hover:text-foreground transition-colors">
          <List className="w-4 h-4" /> Timeline
        </Link>
        <Link href="/workflows" className="flex items-center gap-3 p-2 hover:bg-muted rounded-md font-medium text-muted-foreground hover:text-foreground transition-colors">
          <Target className="w-4 h-4" /> Workflows
        </Link>

        <div className="pt-6 pb-2 text-[10px] text-muted-foreground font-semibold uppercase tracking-wider">Configuration</div>
        <Link href="/settings/api-keys" className="flex items-center gap-3 p-2 hover:bg-muted rounded-md font-medium text-muted-foreground hover:text-foreground transition-colors">
          <Settings className="w-4 h-4" /> API Keys
        </Link>
      </nav>
      <div className="p-4 border-t border-border">
        <Link href="/login" className="flex items-center gap-3 p-2 hover:bg-destructive/10 text-destructive rounded-md font-medium w-full text-left transition-colors">
          <LogOut className="w-4 h-4" /> Logout
        </Link>
      </div>
    </div>
  );
}
