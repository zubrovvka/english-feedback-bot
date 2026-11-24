import pytest
import json
from gemini_parser import extract_json_from_text, sanitize_parsed_schema

def test_extract_json_plain():
    raw = json.dumps({
        "vocab": [{"word": "apple", "translation": "яблоко"}],
        "corrections": [],
        "good_language": [],
        "suggestions": []
    })
    result = extract_json_from_text(raw)
    assert len(result["vocab"]) == 1
    assert result["vocab"][0]["word"] == "apple"
    assert result["corrections"] == []

def test_extract_json_with_markdown_wrapper():
    raw = """Here is your result:
```json
{
  "vocab": [{"word": "book", "translation": "книга"}],
  "corrections": [],
  "good_language": [],
  "suggestions": []
}
```
Hope that helps!"""
    result = extract_json_from_text(raw)
    assert len(result["vocab"]) == 1
    assert result["vocab"][0]["word"] == "book"

def test_extract_json_with_conversational_text():
    raw = """I analyzed your board. Here is the data:
{"vocab": [], "corrections": [{"wrong": "make a party", "correct": "throw a party"}], "good_language": [], "suggestions": []}
Let me know if you need more analysis."""
    result = extract_json_from_text(raw)
    assert len(result["corrections"]) == 1
    assert result["corrections"][0]["correct"] == "throw a party"

def test_extract_json_invalid_raises():
    with pytest.raises((ValueError, json.JSONDecodeError)):
        extract_json_from_text("This is definitely not JSON and has no braces")

def test_extract_json_empty_raises():
    with pytest.raises((ValueError, json.JSONDecodeError)):
        extract_json_from_text("")

def test_sanitize_parsed_schema_valid():
    data = {
        "vocab": [{"word": "cat"}],
        "corrections": [{"wrong": "a", "correct": "b"}],
        "good_language": [{"phrase": "c"}],
        "suggestions": [{"basic": "d", "advanced": "e"}]
    }
    sanitized = sanitize_parsed_schema(data)
    assert len(sanitized["vocab"]) == 1
    assert len(sanitized["corrections"]) == 1
    assert len(sanitized["good_language"]) == 1
    assert len(sanitized["suggestions"]) == 1

def test_sanitize_parsed_schema_missing_and_corrupted_keys():
    data = {
        "vocab": "not a list",
        "corrections": [123, "string", {"wrong": "x", "correct": "y"}],
        # good_language missing
        "suggestions": None
    }
    sanitized = sanitize_parsed_schema(data)
    assert sanitized["vocab"] == []
    assert len(sanitized["corrections"]) == 1
    assert sanitized["corrections"][0]["wrong"] == "x"
    assert sanitized["good_language"] == []
    assert sanitized["suggestions"] == []

def test_sanitize_parsed_schema_non_dict_input():
    for non_dict in [None, [], "string", 42, True]:
        sanitized = sanitize_parsed_schema(non_dict)
        assert sanitized == {"vocab": [], "corrections": [], "good_language": [], "suggestions": []}
