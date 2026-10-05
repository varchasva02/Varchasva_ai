import { Sparkles } from "lucide-react";
import SuggestionCard from "./SuggestionCard";

const SUGGESTIONS = [
  "What projects has Varchasva built?",
  "What technologies does he use?",
  "Tell me about his experience.",
  "What is he currently learning?",
  "Tell me about the PDF RAG Assistant.",
];

interface WelcomeScreenProps {
  onSuggestionClick: (question: string) => void;
}

export default function WelcomeScreen({
  onSuggestionClick,
}: WelcomeScreenProps) {
  return (
    <div className="welcome">
      <div className="welcome-icon">
        <Sparkles />
      </div>

      <h1 className="welcome-title">
        Varchasva <span className="welcome-title-accent">AI</span>
      </h1>

      <p className="welcome-subtitle">
        Ask me anything about Varchasva — his projects, skills, experience, and
        more.
      </p>

      <div className="suggestions">
        {SUGGESTIONS.map((suggestion) => (
          <SuggestionCard
            key={suggestion}
            text={suggestion}
            onClick={onSuggestionClick}
          />
        ))}
      </div>
    </div>
  );
}
