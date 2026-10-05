from google import genai
from dotenv import load_dotenv
import os
import time


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(query, results):
    """Generate an answer using retrieved RAG context."""

    if not results:
        return "I don't have enough information to answer that."

    context_parts = []

    for i, result in enumerate(results, start=1):
        context_parts.append(
            f"""--- Context {i} ---
Source: {result["metadata"].get("source", "unknown")}
Subject: {result["metadata"].get("subject", "unknown")}
Section: {result["metadata"].get("section", "unknown")}

{result["text"]}"""
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are Varchasva AI, a personal portfolio assistant.

Answer the user's question using ONLY the provided context.

Rules:
- Do not invent information.
- Do not use outside knowledge.
- If the context does not contain the answer, say:
  "I don't have that information in my knowledge base."
- Keep the answer clear, natural, and concise.
- When useful, mention relevant project names, technologies, or experience.

CONTEXT:
{context}

USER QUESTION:
{query}
"""

    # Models to attempt (falls back to gemini-3.5-flash-lite if gemini-3.8-flash quota is exhausted)
    models = ["gemini-3.8-flash", "gemini-3.5-flash-lite"]
    last_error = None

    for model_name in models:
        max_attempts = 2 if model_name != models[-1] else 3

        for attempt in range(max_attempts):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                return response.text

            except Exception as e:
                last_error = e
                error_message = str(e)

                # Retry temporary 503/high-demand errors
                if ("503" in error_message or "UNAVAILABLE" in error_message) and attempt < max_attempts - 1:
                    wait_time = 2 ** attempt
                    print(
                        f"Gemini ({model_name}) temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )
                    time.sleep(wait_time)
                    continue

                # If quota is exhausted (429) or retries failed, switch to fallback model
                if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                    print(f"Gemini quota exhausted for {model_name}, trying fallback model...")
                break

    if last_error:
        raise last_error


if __name__ == "__main__":
    print("Gemini generator loaded successfully.")