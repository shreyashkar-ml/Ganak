import React from "react";

type EventEnvelope = {
  id: string;
  type: string;
  session_id: string;
  run_id: string;
  payload: Record<string, unknown>;
};

type Props = {
  events: EventEnvelope[];
};

export function EventStream({ events }: Props) {
  return (
    <div>
      {events.map((event) => (
        <div key={event.id}>
          <strong>{event.type}</strong>
        </div>
      ))}
    </div>
  );
}

