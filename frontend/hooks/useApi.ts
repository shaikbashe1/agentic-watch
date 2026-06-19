import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { Activity, Stats, AgentStat, Alert, Policy, PolicyCreate } from "@/types";

export function useStats() {
  return useQuery({
    queryKey: ["stats"],
    queryFn: async () => {
      const { data } = await api.get<Stats>("/stats");
      return data;
    },
    refetchInterval: 10_000,
  });
}

export function useActivities(limit = 100) {
  return useQuery({
    queryKey: ["activities", limit],
    queryFn: async () => {
      const { data } = await api.get<Activity[]>("/activities", { params: { limit } });
      return data;
    },
    refetchInterval: 10_000,
  });
}

export function useAgentStats() {
  return useQuery({
    queryKey: ["agent-stats"],
    queryFn: async () => {
      const { data } = await api.get<AgentStat[]>("/activities/stats/agents");
      return data;
    },
    refetchInterval: 10_000,
  });
}

export function useAlerts(limit = 100) {
  return useQuery({
    queryKey: ["alerts", limit],
    queryFn: async () => {
      const { data } = await api.get<Alert[]>("/alerts", { params: { limit } });
      return data;
    },
    refetchInterval: 10_000,
  });
}

export function usePolicies() {
  return useQuery({
    queryKey: ["policies"],
    queryFn: async () => {
      const { data } = await api.get<Policy[]>("/policies");
      return data;
    },
  });
}

export function useCreatePolicy() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (policy: PolicyCreate) => {
      const { data } = await api.post<Policy>("/policies", policy);
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["policies"] }),
  });
}

export function useUpdatePolicy() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, updates }: { id: string; updates: Partial<Policy> }) => {
      const { data } = await api.put<Policy>(`/policies/${id}`, updates);
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["policies"] }),
  });
}

export function useDeletePolicy() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      await api.delete(`/policies/${id}`);
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["policies"] }),
  });
}

export function useCreateActivity() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (activity: Omit<Activity, "id" | "timestamp">) => {
      const { data } = await api.post<Activity>("/activities", activity);
      return data;
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["activities"] });
      qc.invalidateQueries({ queryKey: ["stats"] });
      qc.invalidateQueries({ queryKey: ["alerts"] });
    },
  });
}

export function useUpdateAlertStatus() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, status }: { id: number; status: string }) => {
      const { data } = await api.put<Alert>(`/alerts/${id}`, { status });
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["alerts"] }),
  });
}

export function useWebhooks() {
  return useQuery({
    queryKey: ["webhooks"],
    queryFn: async () => {
      const { data } = await api.get<any[]>("/webhooks");
      return data;
    },
  });
}

export function useCreateWebhook() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (webhook: { url: string; secret: string }) => {
      const { data } = await api.post<any>("/webhooks", webhook);
      return data;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["webhooks"] }),
  });
}

export function useDeleteWebhook() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      await api.delete(`/webhooks/${id}`);
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["webhooks"] }),
  });
}
