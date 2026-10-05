import { useRef, useEffect } from "react";
import type { ChatMessage as ChatMessageType } from "../types/chat";
import ChatMessage from "./ChatMessage";
import TypingIndicator from "./TypingIndicator";
import WelcomeScreen from "./WelcomeScreen";

interface ChatWindowProps {
  messages: ChatMessageType[];
  isLoading: boolean;
  onSuggestionClick: (question: string) => void;
  onRetry: (question: string) => void;
}

export default function ChatWindow({
  messages,
  isLoading,
  onSuggestionClick,
  onRetry,
}: ChatWindowProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  if (messages.length === 0 && !isLoading) {
    return <WelcomeScreen onSuggestionClick={onSuggestionClick} />;
  }

  return (
    <div className="chat-messages">
      {messages.map((message) => (
        <ChatMessage
          key={message.id}
          message={message}
          onRetry={message.status === "error" ? onRetry : undefined}
        />
      ))}
      {isLoading && <TypingIndicator />}
      <div ref={messagesEndRef} />
    </div>
  );
}
