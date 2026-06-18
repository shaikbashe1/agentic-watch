"use client";

import { usePolicies, useCreatePolicy, useUpdatePolicy, useDeletePolicy } from "@/hooks/useApi";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useState } from "react";
import { Policy, PolicyCreate } from "@/types";

const EMPTY_FORM: PolicyCreate = { name: "", action_type: "", decision: "allow", is_active: true };

function decisionVariant(d: string) {
  if (d === "block") return "destructive" as const;
  if (d === "warn") return "secondary" as const;
  return "default" as const;
}

export default function PoliciesPage() {
  const { data: policies = [], isLoading, error } = usePolicies();
  const createPolicy = useCreatePolicy();
  const updatePolicy = useUpdatePolicy();
  const deletePolicy = useDeletePolicy();

  const [showForm, setShowForm] = useState(false);
  const [editId, setEditId] = useState<number | null>(null);
  const [form, setForm] = useState<PolicyCreate>(EMPTY_FORM);
  const [formError, setFormError] = useState("");

  const resetForm = () => { setForm(EMPTY_FORM); setEditId(null); setFormError(""); setShowForm(false); };

  const handleSubmit = async () => {
    if (!form.name.trim() || !form.action_type.trim()) {
      setFormError("Name and Action Type are required.");
      return;
    }
    setFormError("");
    if (editId !== null) {
      await updatePolicy.mutateAsync({ id: editId, updates: form });
    } else {
      await createPolicy.mutateAsync(form);
    }
    resetForm();
  };

  const handleEdit = (p: Policy) => {
    setForm({ name: p.name, description: p.description ?? "", action_type: p.action_type, decision: p.decision, is_active: p.is_active });
    setEditId(p.id);
    setShowForm(true);
  };

  const handleToggle = (p: Policy) => {
    updatePolicy.mutate({ id: p.id, updates: { is_active: !p.is_active } });
  };

  const handleDelete = (id: number) => {
    if (confirm("Delete this policy?")) deletePolicy.mutate(id);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">Policies</h1>
        <Button onClick={() => { resetForm(); setShowForm(true); }}>Create Policy</Button>
      </div>

      {showForm && (
        <div className="border rounded-lg p-6 bg-gray-50 space-y-4 max-w-xl">
          <h2 className="font-semibold text-lg">{editId ? "Edit Policy" : "New Policy"}</h2>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-sm font-medium">Name *</label>
              <Input value={form.name} onChange={e => setForm(f => ({ ...f, name: e.target.value }))} placeholder="Policy name" className="mt-1" />
            </div>
            <div>
              <label className="text-sm font-medium">Action Type *</label>
              <Input value={form.action_type} onChange={e => setForm(f => ({ ...f, action_type: e.target.value }))} placeholder="e.g. delete_database" className="mt-1" />
            </div>
          </div>
          <div>
            <label className="text-sm font-medium">Description</label>
            <Input value={form.description ?? ""} onChange={e => setForm(f => ({ ...f, description: e.target.value }))} placeholder="Optional" className="mt-1" />
          </div>
          <div>
            <label className="text-sm font-medium">Decision *</label>
            <select
              value={form.decision}
              onChange={e => setForm(f => ({ ...f, decision: e.target.value as PolicyCreate["decision"] }))}
              className="mt-1 w-full border rounded px-3 py-2 text-sm bg-white"
            >
              <option value="allow">Allow</option>
              <option value="warn">Warn</option>
              <option value="block">Block</option>
            </select>
          </div>
          <label className="flex items-center gap-2 text-sm">
            <input type="checkbox" checked={form.is_active ?? true} onChange={e => setForm(f => ({ ...f, is_active: e.target.checked }))} />
            Active
          </label>
          {formError && <p className="text-red-500 text-sm">{formError}</p>}
          <div className="flex gap-3">
            <Button onClick={handleSubmit} disabled={createPolicy.isPending || updatePolicy.isPending}>
              {editId ? "Update" : "Create"}
            </Button>
            <Button variant="outline" onClick={resetForm}>Cancel</Button>
          </div>
        </div>
      )}

      {error && <div className="text-red-500">Failed to load policies. Is the backend running?</div>}

      <div className="border rounded-md bg-white">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Policy Name</TableHead>
              <TableHead>Action Type</TableHead>
              <TableHead>Decision</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow><TableCell colSpan={5} className="text-center py-4">Loading...</TableCell></TableRow>
            ) : policies.length === 0 ? (
              <TableRow><TableCell colSpan={5} className="text-center py-4 text-muted-foreground">No policies found. Create one above.</TableCell></TableRow>
            ) : policies.map((policy: Policy) => (
              <TableRow key={policy.id}>
                <TableCell className="font-medium">{policy.name}</TableCell>
                <TableCell><code className="text-xs bg-gray-100 px-1 py-0.5 rounded">{policy.action_type}</code></TableCell>
                <TableCell>
                  <Badge variant={decisionVariant(policy.decision)}>{policy.decision.toUpperCase()}</Badge>
                </TableCell>
                <TableCell>
                  <Badge variant={policy.is_active ? "default" : "outline"}>
                    {policy.is_active ? "Active" : "Disabled"}
                  </Badge>
                </TableCell>
                <TableCell>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm" onClick={() => handleEdit(policy)}>Edit</Button>
                    <Button variant="outline" size="sm" onClick={() => handleToggle(policy)}>
                      {policy.is_active ? "Disable" : "Enable"}
                    </Button>
                    <Button variant="destructive" size="sm" onClick={() => handleDelete(policy.id)}>Delete</Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
