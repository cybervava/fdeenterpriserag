from src.rag_prompt import build_rag_prompt


CHUNKS = [
    {"source": "novasense_x500_technical_specification.txt", "text": "X500 range -20°C to 90°C."},
    {"source": "integration_guide_001.txt", "text": "Siemens SCADA via OPC-UA."},
]


def test_includes_numbered_sources_in_order():
    prompt = build_rag_prompt("What is the X500 range?", CHUNKS)

    first = prompt.index("SOURCE 1\nDocument: novasense_x500_technical_specification.txt")
    second = prompt.index("SOURCE 2\nDocument: integration_guide_001.txt")
    assert first < second
    assert "X500 range -20°C to 90°C." in prompt
    assert "Siemens SCADA via OPC-UA." in prompt


def test_includes_question_after_context():
    prompt = build_rag_prompt("What is the X500 range?", CHUNKS)

    assert prompt.index("ENTERPRISE CONTEXT") < prompt.index("USER QUESTION")
    assert prompt.index("USER QUESTION") < prompt.index("What is the X500 range?")


def test_includes_grounding_citation_and_abstention_rules():
    prompt = build_rag_prompt("q", CHUNKS)

    assert "using ONLY the enterprise" in prompt
    assert "Do not invent product capabilities." in prompt
    assert "[Source 1]" in prompt
    assert "does not\n   contain enough information to answer this question." in prompt


def test_handles_no_retrieved_chunks():
    prompt = build_rag_prompt("q", [])

    assert "SOURCE 1" not in prompt
    assert "USER QUESTION" in prompt
