import json
from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data"


def load_json_files():
    documents = []

    for file_path in DATA_DIR.rglob("*.json"):

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        document = {
            "source": str(file_path.relative_to(DATA_DIR)),
            "data": data
        }

        documents.append(document)

    return documents


if __name__ == "__main__":
    documents = load_json_files()

    print(f"Loaded {len(documents)} documents.\n")

    for document in documents:
        print(f"✓ {document['source']}")
