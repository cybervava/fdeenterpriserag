from src.text_cleaner import clean_text


def test_normalizes_windows_and_old_mac_line_endings():
    assert clean_text("a\r\nb\rc") == "a\nb\nc"


def test_collapses_spaces_and_tabs():
    assert clean_text("NovaSense \t  X500") == "NovaSense X500"


def test_collapses_three_or_more_newlines_to_one_blank_line():
    assert clean_text("a\n\n\n\n\nb") == "a\n\nb"


def test_keeps_single_blank_line():
    assert clean_text("a\n\nb") == "a\n\nb"


def test_strips_leading_and_trailing_whitespace():
    assert clean_text("  \n text \n  ") == "text"


def test_empty_string_stays_empty():
    assert clean_text("") == ""
