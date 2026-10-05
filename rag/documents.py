from .loader import load_json_files


def format_value(value, indent=0):
    """Convert nested JSON data into readable text."""

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

    elif isinstance(value, list):
        lines = []

        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(format_value(item, indent + 2))
            else:
                lines.append(f"{' ' * indent}- {item}")

        return "\n".join(lines)

    return str(value)


def create_documents():
    raw_documents = load_json_files()
    documents = []

    for item in raw_documents:
        data = item["data"]
        source = item["source"]

        text = format_value(data)

        documents.append({
            "text": text,
            "metadata": {
                "source": source
            }
        })

    return documents


if __name__ == "__main__":
    documents = create_documents()

    print(f"Created {len(documents)} documents.\n")

    for document in documents:
        print("=" * 60)
        print("SOURCE:", document["metadata"]["source"])
        print("TEXT:")
        print(document["text"][:1000])
        print()
