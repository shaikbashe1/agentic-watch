import Link from 'next/link';
import { LayoutDashboard, List, AlertTriangle, Shield, Target, Users } from 'lucide-react';

export function Sidebar() {
  return (
    <div className="w-64 border-r h-screen bg-gray-50 flex flex-col">
      <div className="p-6 font-bold text-xl flex items-center gap-2 border-b">
        <Shield className="w-6 h-6 text-blue-600" /> Agentic Watch
      </div>
      <div className="p-4 border-b bg-gray-100">
        <div className="text-xs text-gray-500 font-semibold mb-1">CURRENT WORKSPACE</div>
        <select className="w-full bg-white border p-1 rounded text-sm font-medium">
            <option>Acme Corp</option>
            <option>Personal Agents</option>
        </select>
      </div>
      <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
        <Link href="/" className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded font-medium">
          <LayoutDashboard className="w-4 h-4" /> Dashboard
        </Link>
        <Link href="/activities" className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded font-medium">
          <List className="w-4 h-4" /> Activity Logs
        </Link>
        <Link href="/alerts" className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded font-medium">
          <AlertTriangle className="w-4 h-4" /> Alerts
        </Link>
        <Link href="/policies" className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded font-medium">
          <Shield className="w-4 h-4" /> Policies
        </Link>
        <Link href="/goal-alignment" className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded font-medium">
          <Target className="w-4 h-4" /> Goal Alignment
        </Link>
        <Link href="/agents" className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded font-medium">
          <Users className="w-4 h-4" /> Agents
        </Link>
        <Link href="/timeline" className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded font-medium text-purple-600">
          <List className="w-4 h-4" /> Timeline
        </Link>
        <Link href="/workflows" className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded font-medium text-purple-600">
          <LayoutDashboard className="w-4 h-4" /> Workflows
        </Link>
        <Link href="/costs" className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded font-medium text-purple-600">
          <Target className="w-4 h-4" /> Token & Costs
        </Link>
        <Link href="/analytics" className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded font-medium text-purple-600">
          <Target className="w-4 h-4" /> Analytics
        </Link>
        <div className="pt-6 pb-2 text-xs text-gray-500 font-semibold uppercase">Settings</div>
        <Link href="/agents/wizard" className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded font-medium text-gray-700">
          <Target className="w-4 h-4" /> Connect Agent
        </Link>
        <Link href="/settings/api-keys" className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded font-medium text-gray-700">
          <Target className="w-4 h-4" /> API Keys
        </Link>
        <Link href="/settings/team" className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded font-medium text-gray-700">
          <Target className="w-4 h-4" /> Team Management
        </Link>
        <Link href="/settings/billing" className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded font-medium text-gray-700">
          <Target className="w-4 h-4" /> Billing & Plans
        </Link>
      </nav>
      <div className="p-4 border-t">
        <Link href="/login" className="flex items-center gap-2 p-2 hover:bg-red-50 text-red-600 rounded font-medium w-full text-left">
          <Target className="w-4 h-4" /> Logout
        </Link>
      </div>
    </div>
  );
}
