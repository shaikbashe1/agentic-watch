"use client";

import { useWebhooks, useCreateWebhook, useDeleteWebhook } from "@/hooks/useApi";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useState } from "react";
import { Webhook as WebhookIcon } from "lucide-react";

const EMPTY_FORM = { url: "", secret: "" };

export default function WebhooksPage() {
  const { data: webhooks = [], isLoading, error } = useWebhooks();
  const createWebhook = useCreateWebhook();
  const deleteWebhook = useDeleteWebhook();

  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState(EMPTY_FORM);
  const [formError, setFormError] = useState("");

  const resetForm = () => { setForm(EMPTY_FORM); setFormError(""); setShowForm(false); };

  const handleSubmit = async () => {
    if (!form.url.trim() || !form.secret.trim()) {
      setFormError("URL and Secret are required.");
      return;
    }
    
    try {
        new URL(form.url);
    } catch {
        setFormError("Must be a valid URL.");
        return;
    }
    
    setFormError("");
    await createWebhook.mutateAsync(form);
    resetForm();
  };

  const handleDelete = (id: string) => {
    if (confirm("Delete this webhook?")) deleteWebhook.mutate(id);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
            <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
                <WebhookIcon className="h-8 w-8 text-primary" /> Webhooks
            </h1>
            <p className="text-muted-foreground text-sm mt-1">Receive real-time alerts when high-risk events occur.</p>
        </div>
        <Button onClick={() => { resetForm(); setShowForm(true); }}>Add Webhook</Button>
      </div>

      {showForm && (
        <div className="border rounded-lg p-6 bg-card space-y-4 max-w-xl">
          <h2 className="font-semibold text-lg">New Webhook Integration</h2>
          <div>
            <label className="text-sm font-medium">Endpoint URL *</label>
            <Input value={form.url} onChange={e => setForm(f => ({ ...f, url: e.target.value }))} placeholder="https://api.yourcompany.com/alerts" className="mt-1 font-mono text-sm" />
          </div>
          <div>
            <label className="text-sm font-medium">Signing Secret *</label>
            <Input value={form.secret} onChange={e => setForm(f => ({ ...f, secret: e.target.value }))} placeholder="Super secret key for HMAC signature" className="mt-1 font-mono text-sm" type="password" />
            <p className="text-xs text-muted-foreground mt-1">We will use this secret to sign the POST requests so you can verify they came from AgentWatch.</p>
          </div>
          {formError && <p className="text-red-500 text-sm">{formError}</p>}
          <div className="flex gap-3 pt-2">
            <Button onClick={handleSubmit} disabled={createWebhook.isPending}>
              Register Webhook
            </Button>
            <Button variant="outline" onClick={resetForm}>Cancel</Button>
          </div>
        </div>
      )}

      <div className="border border-border rounded-md bg-card">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Webhook URL</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow><TableCell colSpan={3} className="text-center py-4">Loading...</TableCell></TableRow>
            ) : webhooks.length === 0 ? (
              <TableRow><TableCell colSpan={3} className="text-center py-8 text-muted-foreground">No webhooks registered. Add one above.</TableCell></TableRow>
            ) : webhooks.map((wh: any) => (
              <TableRow key={wh.id}>
                <TableCell className="font-mono text-sm text-foreground">{wh.url}</TableCell>
                <TableCell>
                  <Badge variant={wh.is_active ? "default" : "outline"}>
                    {wh.is_active ? "Active" : "Disabled"}
                  </Badge>
                </TableCell>
                <TableCell>
                  <Button variant="destructive" size="sm" onClick={() => handleDelete(wh.id)}>Delete</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
