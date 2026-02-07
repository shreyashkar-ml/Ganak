import { apiGet } from "../api/client";

type EventEnvelope = {
  id: string;
  type: string;
  session_id: string;
  run_id: string;
  payload: Record<string, unknown>;
};

export async function getSessionEvents(
  sessionId: string,
  onEvents: (events: EventEnvelope[]) => void
) {
  const data = await apiGet(`/events/${sessionId}`);
  onEvents(data.events || []);
}

