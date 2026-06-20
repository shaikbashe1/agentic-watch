import { randomUUID } from "crypto";

interface AgentWatchOptions {
  apiKey?: string;
  apiUrl?: string;
  flushIntervalMs?: number;
}

export class AgentWatchClient {
  private static instance: AgentWatchClient | null = null;
  private apiKey: string;
  private apiUrl: string;
  private flushIntervalMs: number;
  private eventBuffer: any[] = [];
  private flushTimer: NodeJS.Timeout | null = null;
  private isShuttingDown = false;

  private constructor(options: AgentWatchOptions) {
    this.apiKey = options.apiKey || process.env.AGENTWATCH_API_KEY || "";
    this.apiUrl = options.apiUrl || process.env.AGENTWATCH_API_URL || "https://backend-psi-two-49.vercel.app";
    this.flushIntervalMs = options.flushIntervalMs || 2000;

    if (!this.apiKey) {
      console.warn("[AgentWatch] Warning: No API key provided. Telemetry will not be recorded.");
    }

    this.startFlushTimer();
  }

  public static init(options: AgentWatchOptions = {}): AgentWatchClient {
    if (!AgentWatchClient.instance) {
      AgentWatchClient.instance = new AgentWatchClient(options);
    }
    return AgentWatchClient.instance;
  }

  public static getInstance(): AgentWatchClient {
    if (!AgentWatchClient.instance) {
      return AgentWatchClient.init();
    }
    return AgentWatchClient.instance;
  }

  public recordEvent(event: any) {
    if (this.isShuttingDown || !this.apiKey) return;
    this.eventBuffer.push(event);
  }

  private startFlushTimer() {
    this.flushTimer = setInterval(() => {
      this.flush();
    }, this.flushIntervalMs);
  }

  public async flush() {
    if (this.eventBuffer.length === 0 || !this.apiKey) return;

    const eventsToFlush = [...this.eventBuffer];
    this.eventBuffer = [];

    try {
      const response = await fetch(`${this.apiUrl}/ingest/batch`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${this.apiKey}`,
        },
        body: JSON.stringify({ events: eventsToFlush }),
      });

      if (!response.ok) {
        console.error(`[AgentWatch] Failed to flush events: ${response.statusText}`);
      }
    } catch (error) {
      console.error("[AgentWatch] Error flushing events", error);
    }
  }

  public async shutdown() {
    this.isShuttingDown = true;
    if (this.flushTimer) {
      clearInterval(this.flushTimer);
    }
    await this.flush();
  }
}
