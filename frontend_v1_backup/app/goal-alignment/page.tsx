"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Target, AlertCircle } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";
import { AlignmentResponse } from "@/types";
import { Badge } from "@/components/ui/badge";

export default function GoalAlignmentPage() {
  const [goal, setGoal] = useState("");
  const [action, setAction] = useState("");
  const [result, setResult] = useState<AlignmentResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const testAlignment = async () => {
    setLoading(true);
    try {
      const { data } = await api.post<AlignmentResponse>("/alignments", {
        user_goal: goal,
        agent_action: action
      });
      setResult(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Goal Alignment Analysis</h1>
      
      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Test Alignment</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium">User Goal</label>
              <Input value={goal} onChange={e => setGoal(e.target.value)} placeholder="e.g. Build Student Portal" className="mt-1" />
            </div>
            <div>
              <label className="text-sm font-medium">Agent Action</label>
              <Input value={action} onChange={e => setAction(e.target.value)} placeholder="e.g. Delete Production Database" className="mt-1" />
            </div>
            <Button onClick={testAlignment} disabled={loading} className="w-full">
              {loading ? "Analyzing..." : "Analyze Alignment"}
            </Button>
          </CardContent>
        </Card>

        {result && (
          <Card>
            <CardHeader>
              <CardTitle>Analysis Result</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between items-center p-4 border rounded-lg bg-gray-50">
                <div className="flex items-center gap-2">
                  <Target className="w-5 h-5 text-blue-500" />
                  <span className="font-semibold">Alignment Score</span>
                </div>
                <span className="text-2xl font-bold text-blue-600">{result.alignment_score}/100</span>
              </div>
              <div className="flex justify-between items-center p-4 border rounded-lg bg-gray-50">
                <div className="flex items-center gap-2">
                  <AlertCircle className="w-5 h-5 text-red-500" />
                  <span className="font-semibold">Risk Score</span>
                </div>
                <span className="text-2xl font-bold text-red-600">{result.risk_score}/100</span>
              </div>
              <div className="p-4 border rounded-lg">
                <div className="flex justify-between mb-2">
                  <span className="font-semibold">Decision</span>
                  <Badge variant={result.safe ? 'default' : 'destructive'}>
                    {result.safe ? 'SAFE' : 'UNSAFE'}
                  </Badge>
                </div>
                <p className="text-sm text-gray-600">{result.reason}</p>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
