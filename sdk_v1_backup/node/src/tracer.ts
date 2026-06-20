import { AsyncLocalStorage } from "async_hooks";
import { randomUUID } from "crypto";
import { AgentWatchClient } from "./client";

export interface TraceContext {
  traceId: string;
  spanId: string;
}

const traceContextStorage = new AsyncLocalStorage<TraceContext>();

export function getTraceContext(): TraceContext | undefined {
  return traceContextStorage.getStore();
}

interface TraceOptions {
  name: string;
  eventType?: string;
  metadata?: Record<string, any>;
}

/**
 * Higher-order function to trace any async execution.
 * It tracks latency, success/failure, and automatically manages the DAG span hierarchy.
 */
export function withTrace<T extends (...args: any[]) => Promise<any>>(
  options: TraceOptions,
  fn: T
): T {
  return (async (...args: any[]) => {
    const parentContext = traceContextStorage.getStore();
    
    // If no parent context exists, this is the root of a new trace
    const traceId = parentContext?.traceId || randomUUID();
    const spanId = randomUUID();
    const parentSpanId = parentContext?.spanId;
    
    const startTime = Date.now();
    
    const newContext: TraceContext = { traceId, spanId };

    try {
      // Run the wrapped function within the new AsyncLocalStorage context
      const result = await traceContextStorage.run(newContext, () => fn(...args));
      
      const latencyMs = Date.now() - startTime;
      
      // Record successful event
      AgentWatchClient.getInstance().recordEvent({
        trace_id: traceId,
        span_id: spanId,
        parent_span_id: parentSpanId,
        event_type: options.eventType || "function_call",
        payload: {
          name: options.name,
          args: args,
          result: result,
          ...options.metadata
        },
        latency_ms: latencyMs
      });

      return result;
    } catch (error) {
      const latencyMs = Date.now() - startTime;
      
      // Record failed event
      AgentWatchClient.getInstance().recordEvent({
        trace_id: traceId,
        span_id: spanId,
        parent_span_id: parentSpanId,
        event_type: "error",
        payload: {
          name: options.name,
          error: error instanceof Error ? error.message : String(error),
          ...options.metadata
        },
        latency_ms: latencyMs
      });

      throw error;
    }
  }) as T;
}
