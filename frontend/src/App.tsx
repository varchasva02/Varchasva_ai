import { useState, useEffect, useCallback } from "react";
import "./App.css";
import type { ChatMessage } from "./types/chat";
import { askVarchasva, checkHealth } from "./services/api";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";

function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

export default function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [healthStatus, setHealthStatus] = useState<"checking" | "online" | "offline">("checking");

  // Health-check backend root endpoint immediately and every 30 seconds
  useEffect(() => {
    let isMounted = true;

    const performHealthCheck = async () => {
      const online = await checkHealth();
      if (isMounted) {
        setHealthStatus(online ? "online" : "offline");
      }
    };

    performHealthCheck();
    const intervalId = setInterval(performHealthCheck, 30_000);

    return () => {
      isMounted = false;
      clearInterval(intervalId);
    };
  }, []);

  const sendMessage = useCallback(
    async (question: string) => {
      if (isLoading || !question.trim()) return;

      const userMessage: ChatMessage = {
        id: generateId(),
        role: "user",
        content: question,
        timestamp: new Date(),
        status: "sent",
      };

      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);

      try {
        const answer = await askVarchasva(question);

        const assistantMessage: ChatMessage = {
          id: generateId(),
          role: "assistant",
          content: answer,
          timestamp: new Date(),
          status: "sent",
        };

        setMessages((prev) => [...prev, assistantMessage]);
        setHealthStatus("online");
      } catch (error) {
        const errorMessage =
          error instanceof Error
            ? error.message
            : "Something went wrong. Please try again.";

        const assistantError: ChatMessage = {
          id: generateId(),
          role: "assistant",
          content: errorMessage,
          timestamp: new Date(),
          status: "error",
        };

        setMessages((prev) => [...prev, assistantError]);

        // If it was a connection error, mark as offline
        if (
          errorMessage.toLowerCase().includes("connect") ||
          errorMessage.toLowerCase().includes("server") ||
          errorMessage.toLowerCase().includes("failed to fetch")
        ) {
          setHealthStatus("offline");
        }
      } finally {
        setIsLoading(false);
      }
    },
    [isLoading]
  );

  const handleRetry = useCallback(
    (errorContent: string) => {
      // Find the user message that preceded this error
      setMessages((prev) => {
        // Remove the error message
        const withoutError = prev.filter(
          (m) => !(m.role === "assistant" && m.content === errorContent && m.status === "error")
        );
        return withoutError;
      });

      // Find the last user message to retry
      const lastUserMsg = [...messages]
        .reverse()
        .find((m) => m.role === "user");
      if (lastUserMsg) {
        sendMessage(lastUserMsg.content);
      }
    },
    [messages, sendMessage]
  );

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-brand">
          <h1 className="header-logo">
            Varchasva <span className="header-logo-accent">AI</span>
          </h1>
          <span className="header-tagline">Personal AI Assistant</span>
        </div>

        <div className="header-right">
          <div className="header-status">
            <span
              className={`status-dot ${
                healthStatus === "offline"
                  ? "status-dot--offline"
                  : healthStatus === "checking"
                  ? "status-dot--checking"
                  : ""
              }`}
            />
            {healthStatus === "offline"
              ? "OFFLINE"
              : healthStatus === "online"
              ? "ONLINE"
              : "CHECKING..."}
          </div>
        </div>
      </header>

      {/* Chat */}
      <div className="chat-container">
        <ChatWindow
          messages={messages}
          isLoading={isLoading}
          onSuggestionClick={sendMessage}
          onRetry={handleRetry}
        />
      </div>

      {/* Input */}
      <ChatInput onSend={sendMessage} isLoading={isLoading} />
    </div>
  );
}
