export interface Activity {
  id: number;
  agent_name: string;
  action_type: string;
  action_description: string;
  target_resource: string;
  status: string;
  metadata?: Record<string, unknown>;
  timestamp: string;
  risk_score?: number | null;
  alignment_score?: number | null;
  policy_decision?: string | null;
}

export interface Stats {
  total: number;
  success: number;
  warning: number;
  blocked: number;
  failed: number;
}

export interface AgentStat {
  agent_name: string;
  total: number;
}

export type AlertSeverity = "low" | "medium" | "high" | "critical";
export type AlertStatus = "open" | "acknowledged" | "resolved";

export interface Alert {
  id: number;
  title: string;
  description?: string | null;
  severity: AlertSeverity;
  source: string;
  activity_id?: number | null;
  status: AlertStatus;
  created_at: string;
}

export interface Policy {
  id: number;
  name: string;
  description?: string | null;
  action_type: string;
  decision: "allow" | "warn" | "block";
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface PolicyCreate {
  name: string;
  description?: string;
  action_type: string;
  decision: "allow" | "warn" | "block";
  is_active?: boolean;
}

export interface AlignmentResponse {
  safe: boolean;
  alignment_score: number;
  risk_score: number;
  reason: string;
}
