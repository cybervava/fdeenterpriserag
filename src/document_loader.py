from pathlib import Path


def load_documents(data_directory):

    data_path = Path(
        data_directory
    )

    documents = []

    for file_path in data_path.rglob(
        "*.txt"
    ):

        text = file_path.read_text(
            encoding="utf-8"
        )

        documents.append({
            "text": text,
            "filename": file_path.name,
            "source": str(file_path)
        })

    return documents
