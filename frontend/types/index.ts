export interface Activity {
  id: number;
  agent_name: string;
  action_type: string;
  action_description: string;
  target_resource: string;
  status: string;
  metadata?: any;
  timestamp: string;
}

export interface Stats {
  total: number;
  success: number;
  warning: number;
  blocked: number;
  failed: number;
}

export interface Alert {
  id: number;
  severity: "Low" | "Medium" | "High" | "Critical";
  message: string;
  timestamp: string;
}

export interface Policy {
  id: number;
  name: string;
  enabled: boolean;
}

export interface AlignmentResponse {
  safe: boolean;
  alignment_score: number;
  risk_score: number;
  reason: string;
}
