import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { Activity, Stats, Alert, Policy } from "@/types";

export function useStats() {
  return useQuery({
    queryKey: ["stats"],
    queryFn: async () => {
      const { data } = await api.get<Stats>("/stats");
      return data;
    },
  });
}

export function useActivities() {
  return useQuery({
    queryKey: ["activities"],
    queryFn: async () => {
      const { data } = await api.get<Activity[]>("/activities");
      return data;
    },
  });
}

export function useAlerts() {
  return useQuery({
    queryKey: ["alerts"],
    queryFn: async () => {
      const { data } = await api.get<Alert[]>("/alerts");
      return data;
    },
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
