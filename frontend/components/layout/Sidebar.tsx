import Link from 'next/link';
import { LayoutDashboard, List, AlertTriangle, Shield, Target, Users } from 'lucide-react';

export function Sidebar() {
  return (
    <div className="w-64 border-r h-screen bg-gray-50 flex flex-col">
      <div className="p-6 font-bold text-xl flex items-center gap-2 border-b">
        <Shield className="w-6 h-6 text-blue-600" /> Agentic Watch
      </div>
      <nav className="flex-1 p-4 space-y-1">
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
      </nav>
    </div>
  );
}
