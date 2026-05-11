import os


def load_documents(data_dir="data/raw"):
    documents = []

    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            path = os.path.join(data_dir, filename)

            with open(path, "r", encoding="utf-8") as file:
                text = file.read()

            documents.append({
                "source": filename,
                "content": text
            })

    return documents


if __name__ == "__main__":
    docs = load_documents()

    print(f"Loaded {len(docs)} documents")

    for doc in docs:
        print(f"- {doc['source']}")
