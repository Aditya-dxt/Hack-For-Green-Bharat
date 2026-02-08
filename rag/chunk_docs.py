import os

# Path to your documents folder
DOCS_PATH = "docs"

def load_and_chunk_documents():
    chunks = []

    # Go through each file in docs folder
    for filename in os.listdir(DOCS_PATH):
        file_path = os.path.join(DOCS_PATH, filename)

        # Read only .txt files
        if filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

                # Split by new lines
                lines = text.split("\n")

                for line in lines:
                    clean_line = line.strip()
                    if clean_line:
                        chunks.append({
                            "text": clean_line,
                            "source": filename
                        })

    return chunks


if __name__ == "__main__":
    chunks = load_and_chunk_documents()

    print("TOTAL CHUNKS:", len(chunks))
    print("-" * 40)

    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i}:")
        print(chunk["text"])
        print("Source:", chunk["source"])
        print("-" * 40)
