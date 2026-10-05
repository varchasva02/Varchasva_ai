from .loader import load_json_files


def format_value(value, indent=0):
    """Convert nested JSON values into readable text."""

    if isinstance(value, dict):
        lines = []

        for key, val in value.items():
            title = key.replace("_", " ").title()

            if isinstance(val, (dict, list)):
                lines.append(f"{' ' * indent}{title}:")
                lines.append(format_value(val, indent + 2))
            else:
                lines.append(f"{' ' * indent}{title}: {val}")

        return "\n".join(lines)

    if isinstance(value, list):
        lines = []

        for item in value:
            if isinstance(item, dict):
                lines.append(format_value(item, indent + 2))
            else:
                lines.append(f"{' ' * indent}- {item}")

        return "\n".join(lines)

    return str(value)


def get_project_chunks(data, source):
    """Create meaningful chunks for a project."""

    name = data.get("name", "Unknown Project")
    category = data.get("category", "")
    status = data.get("status", "")

    chunks = []

    # 1. Overview
    overview = {
        "Type": data.get("type"),
        "Description": data.get("description")
    }

    chunks.append({
        "text": (
            f"Project: {name}\n"
            f"Category: {category}\n"
            f"Status: {status}\n\n"
            f"{format_value(overview)}"
        ),
        "metadata": {
            "source": source,
            "subject": name,
            "section": "overview",
            "category": category,
            "status": status
        }
    })

    # 2. Technical information
    technical = {}

    if "technologies" in data:
        technical["Technologies"] = data["technologies"]

    if "features" in data:
        technical["Features"] = data["features"]

    if "technical_workflow" in data:
        technical["Technical Workflow"] = data["technical_workflow"]

    if technical:
        chunks.append({
            "text": (
                f"Project: {name}\n"
                f"Category: {category}\n\n"
                f"{format_value(technical)}"
            ),
            "metadata": {
                "source": source,
                "subject": name,
                "section": "technical",
                "category": category,
                "status": status
            }
        })

    # 3. Role and learning
    learning = {}

    if "role" in data:
        learning["Role"] = data["role"]

    if "learning_outcomes" in data:
        learning["Learning Outcomes"] = data["learning_outcomes"]

    if learning:
        chunks.append({
            "text": (
                f"Project: {name}\n\n"
                f"{format_value(learning)}"
            ),
            "metadata": {
                "source": source,
                "subject": name,
                "section": "role_and_learning",
                "category": category,
                "status": status
            }
        })

    return chunks


def create_semantic_chunks():
    raw_documents = load_json_files()
    chunks = []

    for document in raw_documents:
        data = document["data"]
        source = document["source"]

        # Data policy is application-level configuration,
        # not knowledge for semantic retrieval.
        if source == "data-policy.json":
            continue

        # Project files get project-specific chunking.
        if source.startswith("projects/"):
            chunks.extend(get_project_chunks(data, source))
            continue

        # Smaller profile/experience/link documents stay together.
        filename = source.split("/")[-1]
        subject = filename.replace(".json", "").replace("-", " ").title()

        if "name" in data:
            subject = data["name"]

        text = (
            f"Subject: {subject}\n\n"
            f"{format_value(data)}"
        )

        chunks.append({
            "text": text,
            "metadata": {
                "source": source,
                "subject": subject,
                "section": "complete"
            }
        })

    return chunks


if __name__ == "__main__":
    chunks = create_semantic_chunks()

    print(f"Created {len(chunks)} semantic chunks.\n")

    for chunk in chunks:
        print("=" * 70)
        print("SOURCE:", chunk["metadata"]["source"])
        print("SUBJECT:", chunk["metadata"]["subject"])
        print("SECTION:", chunk["metadata"]["section"])
        print()
        print(chunk["text"])
        print()
