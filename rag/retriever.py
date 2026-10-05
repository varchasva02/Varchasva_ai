import re

from .embedder import get_embedding_model
from .vector_store import build_vector_store


def tokenize(text):
    """Convert text into lowercase keywords."""
    return set(
        re.findall(
            r"\b[a-zA-Z0-9][a-zA-Z0-9+#.-]*\b",
            text.lower()
        )
    )


def keyword_score(query, text):
    """Calculate keyword overlap."""
    query_words = tokenize(query)
    text_words = tokenize(text)

    if not query_words:
        return 0.0

    overlap = query_words.intersection(text_words)

    return len(overlap) / len(query_words)


def detect_intent(query):
    """Detect the likely information section requested."""

    query = query.lower()

    intents = {
        "technical": [
            "technology",
            "technologies",
            "tech stack",
            "tools",
            "framework",
            "how does",
            "how it works",
            "workflow",
            "implemented",
            "implementation",
            "built using",
            "used for"
        ],

        "experience": [
            "internship",
            "interned",
            "intern",
            "company",
            "work experience",
            "worked at",
            "worked for"
        ],

        "currently-learning": [
            "currently learning",
            "learning",
            "studying",
            "learning now",
            "improving"
        ],

        "projects": [
            "projects",
            "project",
            "built",
            "developed",
            "created",
            "made"
        ],

        "education": [
            "education",
            "degree",
            "college",
            "university",
            "studying at",
            "course"
        ],

        "certifications": [
            "certification",
            "certifications",
            "certificate",
            "certificates"
        ],
        "featured-projects": [
        "featured",
        "featured projects",
        "featured project",
        "featured on portfolio",
        "portfolio projects",
        "main projects",
        "highlighted projects",
        "highlighted project"
        ],

        "experimental-projects": [
        "experimental projects",
        "experimental project",
        "experimental work",
        "experiments",
        "experimental"
        ],
        "all-projects": [
        "what projects",
        "which projects",
        "list projects",
        "all projects",
        "his projects",
        "her projects",
        "projects has varchasva built",
        "projects has varchasva worked on",
        "projects in his portfolio",
        "projects in varchasva's portfolio",
        "tell me about his projects"
        ]
    }

    detected = []

    for intent, keywords in intents.items():
        for keyword in keywords:
            if keyword in query:
                detected.append(intent)
                break

    return detected
    if "featured-projects" in detected:
        detected = [i for i in detected if i != "all-projects"]

    if "experimental-projects" in detected:
        detected = [i for i in detected if i != "all-projects"]

def source_matches_intent(source, intents):
    """Check whether a source belongs to the requested information domain."""

    if not intents:
        return True

    for intent in intents:

        if intent == "projects":
            if "projects/" in source or source == "links/project-links.json":
                return True

        elif intent == "technical":
            if "projects/" in source:
                return True

        elif intent == "experience":
            if "experience/" in source:
                return True

        elif intent == "currently-learning":
            if "currently-learning" in source:
                return True

        elif intent == "education":
            if "education" in source:
                return True

        elif intent == "certifications":
            if "certifications" in source:
                return True

    return False


def intent_boost(query, metadata):
    """Give a small boost to chunks matching the query intent."""

    intents = detect_intent(query)

    section = metadata.get("section", "")
    source = metadata.get("source", "")

    boost = 0.0

    # Technical questions → technical project sections
    if "technical" in intents and section == "technical":
        boost += 0.15

    # Experience questions → experience data
    if "experience" in intents and "experience/" in source:
        boost += 0.15

    # Learning questions → currently-learning data
    if "currently-learning" in intents:
        if "currently-learning" in source:
            boost += 0.20

    # Project questions → project chunks
    if "projects" in intents and "projects/" in source:
        boost += 0.15

    # Education questions → education data
    if "education" in intents and "education" in source:
        boost += 0.20

    # Certification questions → certification data
    if "certifications" in intents and "certifications" in source:
        boost += 0.20

    # Featured project questions
    if "featured-projects" in intents:
        if "projects/featured/" in source:
            boost += 0.25

    # Experimental project questions
    if "experimental-projects" in intents:
        if "projects/experimental/" in source:
            boost += 0.25      
    

    # Broad project-list questions → project links / complete project list
    if "all-projects" in intents:
        if "project-links" in source:
            boost += 0.30
    return boost


def retrieve(query, top_k=5):

    index, chunks = build_vector_store()

    model = get_embedding_model()

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    intents = detect_intent(query)

    # Search all chunks first.
    # Our dataset is currently small, so this is fine.
    candidate_k = len(chunks)

    semantic_scores, indices = index.search(
        query_embedding,
        candidate_k
    )

    results = []

    for semantic_score, index_position in zip(
        semantic_scores[0],
        indices[0]
    ):

        if index_position == -1:
            continue

        chunk = chunks[index_position]

        source = chunk["metadata"].get("source", "")

        # Route retrieval to the relevant knowledge domain
        if not source_matches_intent(source, intents):
            continue

        semantic_score = float(semantic_score)

        lexical_score = keyword_score(
            query,
            chunk["text"]
        )

        boost = intent_boost(
            query,
            chunk["metadata"]
        )

        final_score = (
            0.65 * semantic_score
            + 0.20 * lexical_score
            + boost
        )

        results.append({
            "score": final_score,
            "semantic_score": semantic_score,
            "keyword_score": lexical_score,
            "intent_boost": boost,
            "text": chunk["text"],
            "metadata": chunk["metadata"]
        })

    results.sort(
        key=lambda result: result["score"],
        reverse=True
    )

    return results[:top_k]


if __name__ == "__main__":

    query = input("\nAsk Varchasva AI: ")

    print("\nDetected intents:", detect_intent(query))

    results = retrieve(query)

    print("\n" + "=" * 70)
    print("HYBRID + INTENT RETRIEVAL RESULTS")
    print("=" * 70)

    for i, result in enumerate(results, start=1):

        print(f"\nResult {i}")
        print("-" * 70)

        print(f"Final score:    {result['score']:.4f}")
        print(f"Semantic score: {result['semantic_score']:.4f}")
        print(f"Keyword score:  {result['keyword_score']:.4f}")
        print(f"Intent boost:   {result['intent_boost']:.4f}")

        print(f"Source:   {result['metadata']['source']}")
        print(f"Subject:  {result['metadata']['subject']}")
        print(f"Section:  {result['metadata']['section']}")

        print("\n" + result["text"])