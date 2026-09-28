from src.document_loader import load_documents


def test_loads_txt_files_recursively_with_metadata(tmp_path):
    (tmp_path / "products").mkdir()
    (tmp_path / "products" / "x500.txt").write_text("X500 spec", encoding="utf-8")
    (tmp_path / "faq.txt").write_text("FAQ °C", encoding="utf-8")
    (tmp_path / "notes.md").write_text("ignored", encoding="utf-8")

    documents = load_documents(tmp_path)
    by_name = {doc["filename"]: doc for doc in documents}

    assert set(by_name) == {"x500.txt", "faq.txt"}
    assert by_name["x500.txt"]["text"] == "X500 spec"
    assert by_name["x500.txt"]["source"] == str(tmp_path / "products" / "x500.txt")
    assert by_name["faq.txt"]["text"] == "FAQ °C"


def test_empty_directory_returns_no_documents(tmp_path):
    assert load_documents(tmp_path) == []
