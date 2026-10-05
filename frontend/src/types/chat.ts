export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  status?: "sending" | "sent" | "error";
}

export interface AskRequest {
  question: string;
}

export interface AskResponse {
  question: string;
  answer: string;
}

export interface ApiErrorResponse {
  error: string;
  details?: string;
}
