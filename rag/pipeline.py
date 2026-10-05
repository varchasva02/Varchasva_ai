from .retriever import retrieve
from .generator import generate_answer


def ask_varchasva(query):
    """Retrieve relevant context and generate an answer."""

    results = retrieve(query, top_k=5)

    answer = generate_answer(query, results)

    return answer


if __name__ == "__main__":

    query = input("\nAsk Varchasva AI: ")

    print("\nThinking...\n")

    answer = ask_varchasva(query)

    print("=" * 70)
    print("VARCHASVA AI")
    print("=" * 70)
    print(answer)
