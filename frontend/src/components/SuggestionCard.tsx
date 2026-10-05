import { ArrowUp } from "lucide-react";

interface SuggestionCardProps {
  text: string;
  onClick: (text: string) => void;
}

export default function SuggestionCard({ text, onClick }: SuggestionCardProps) {
  return (
    <button
      className="suggestion-card"
      onClick={() => onClick(text)}
      type="button"
    >
      <ArrowUp />
      {text}
    </button>
  );
}
