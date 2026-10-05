import type { ChatMessage as ChatMessageType } from "../types/chat";
import { RotateCcw } from "lucide-react";
import ReactMarkdown from "react-markdown";

interface ChatMessageProps {
  message: ChatMessageType;
  onRetry?: (content: string) => void;
}

export default function ChatMessage({ message, onRetry }: ChatMessageProps) {
  const isError = message.status === "error";
  const isAssistant = message.role === "assistant";

  return (
    <div
      className={`message message--${message.role}${isError ? " message--error" : ""}`}
    >
      <span className="message-label">
        {message.role === "user" ? "You" : "Varchasva AI"}
      </span>

      <div className="message-bubble">
        {isAssistant ? (
          <div className="markdown-content">
            <ReactMarkdown
              components={{
                a: ({ ...props }) => (
                  <a {...props} target="_blank" rel="noopener noreferrer" />
                ),
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        ) : (
          message.content
        )}
      </div>

      {isError && onRetry && (
        <div className="message-error-actions">
          <button
            className="retry-button"
            onClick={() => onRetry(message.content)}
            type="button"
          >
            <RotateCcw />
            Retry
          </button>
        </div>
      )}
    </div>
  );
}

