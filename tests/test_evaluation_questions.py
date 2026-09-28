from tests.evaluation_questions import EVALUATION_QUESTIONS


def test_every_question_has_a_ground_truth_source():
    assert len(EVALUATION_QUESTIONS) == 5
    for item in EVALUATION_QUESTIONS:
        assert item["question"].strip()
        assert item["expected_keyword"].strip()
        assert ("expected_source" in item) != ("expected_source_contains" in item)
