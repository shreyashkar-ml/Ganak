import React, { useEffect, useState } from "react";
import { EventStream } from "../../components/EventStream";
import { getSessionEvents } from "../../streaming/ws";

type EventEnvelope = {
  id: string;
  type: string;
  session_id: string;
  run_id: string;
  payload: Record<string, unknown>;
};

export default function SessionPage() {
  const [events, setEvents] = useState<EventEnvelope[]>([]);

  useEffect(() => {
    getSessionEvents("session", (evt) => setEvents(evt));
  }, []);

  return (
    <main>
      <h1>Session</h1>
      <EventStream events={events} />
    </main>
  );
}

