"use client";

import { usePolicies, useCreatePolicy, useUpdatePolicy, useDeletePolicy } from "@/hooks/useApi";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useState } from "react";
import { Textarea } from "@/components/ui/textarea";

const EMPTY_FORM = { name: "", description: "", action: "BLOCK", conditions: '{"field": "request.model", "operator": "==", "value": "gpt-4"}', is_active: true };

function actionVariant(a: string) {
  if (a === "BLOCK") return "destructive" as const;
  if (a === "REDACT") return "secondary" as const;
  return "default" as const;
}

export default function PoliciesPage() {
  const { data: policies = [], isLoading, error } = usePolicies();
  const createPolicy = useCreatePolicy();
  const updatePolicy = useUpdatePolicy();
  const deletePolicy = useDeletePolicy();

  const [showForm, setShowForm] = useState(false);
  const [editId, setEditId] = useState<string | null>(null);
  const [form, setForm] = useState(EMPTY_FORM);
  const [formError, setFormError] = useState("");

  const resetForm = () => { setForm(EMPTY_FORM); setEditId(null); setFormError(""); setShowForm(false); };

  const handleSubmit = async () => {
    if (!form.name.trim()) {
      setFormError("Name is required.");
      return;
    }
    
    let parsedConditions;
    try {
        parsedConditions = JSON.parse(form.conditions);
    } catch (e) {
        setFormError("Conditions must be valid JSON.");
        return;
    }
    
    setFormError("");
    const payload = {
        name: form.name,
        description: form.description,
        action: form.action,
        conditions: parsedConditions,
        is_active: form.is_active
    };

    if (editId !== null) {
      await updatePolicy.mutateAsync({ id: editId, updates: payload });
    } else {
      await createPolicy.mutateAsync(payload);
    }
    resetForm();
  };

  const handleEdit = (p: any) => {
    setForm({ 
        name: p.name, 
        description: p.description ?? "", 
        action: p.action, 
        conditions: JSON.stringify(p.conditions, null, 2), 
        is_active: p.is_active 
    });
    setEditId(p.id);
    setShowForm(true);
  };

  const handleToggle = (p: any) => {
    updatePolicy.mutate({ id: p.id, updates: { is_active: !p.is_active } });
  };

  const handleDelete = (id: string) => {
    if (confirm("Delete this policy?")) deletePolicy.mutate(id);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">Advanced Policies</h1>
        <Button onClick={() => { resetForm(); setShowForm(true); }}>Create Policy</Button>
      </div>

      {showForm && (
        <div className="border rounded-lg p-6 bg-card space-y-4 max-w-xl">
          <h2 className="font-semibold text-lg">{editId ? "Edit Policy" : "New Policy"}</h2>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-sm font-medium">Name *</label>
              <Input value={form.name} onChange={e => setForm(f => ({ ...f, name: e.target.value }))} placeholder="Policy name" className="mt-1" />
            </div>
            <div>
              <label className="text-sm font-medium">Action *</label>
              <select
                value={form.action}
                onChange={e => setForm(f => ({ ...f, action: e.target.value }))}
                className="mt-1 w-full border rounded px-3 py-2 text-sm bg-background text-foreground"
              >
                <option value="BLOCK">BLOCK</option>
                <option value="REDACT">REDACT</option>
                <option value="ALERT">ALERT</option>
              </select>
            </div>
          </div>
          <div>
            <label className="text-sm font-medium">Description</label>
            <Input value={form.description} onChange={e => setForm(f => ({ ...f, description: e.target.value }))} placeholder="Optional" className="mt-1" />
          </div>
          <div>
            <label className="text-sm font-medium">Conditions (JSON AST)</label>
            <Textarea 
                value={form.conditions} 
                onChange={e => setForm(f => ({ ...f, conditions: e.target.value }))} 
                className="mt-1 font-mono text-xs" 
                rows={5} 
            />
          </div>
          <label className="flex items-center gap-2 text-sm">
            <input type="checkbox" checked={form.is_active} onChange={e => setForm(f => ({ ...f, is_active: e.target.checked }))} />
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

      <div className="border border-border rounded-md bg-card">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Policy Name</TableHead>
              <TableHead>Action</TableHead>
              <TableHead>Conditions</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow><TableCell colSpan={5} className="text-center py-4">Loading...</TableCell></TableRow>
            ) : policies.length === 0 ? (
              <TableRow><TableCell colSpan={5} className="text-center py-4 text-muted-foreground">No policies found.</TableCell></TableRow>
            ) : policies.map((policy: any) => (
              <TableRow key={policy.id}>
                <TableCell className="font-medium text-foreground">{policy.name}</TableCell>
                <TableCell>
                  <Badge variant={actionVariant(policy.action)}>{policy.action}</Badge>
                </TableCell>
                <TableCell><code className="text-xs bg-muted text-muted-foreground px-1 py-0.5 rounded truncate max-w-[200px] block">{JSON.stringify(policy.conditions)}</code></TableCell>
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
