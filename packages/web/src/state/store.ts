import { useState } from "react";

type SessionState = {
  sessionId: string | null;
};

export function useSessionState() {
  const [state, setState] = useState<SessionState>({ sessionId: null });
  return { state, setState };
}

