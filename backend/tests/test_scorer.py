import json
import pytest
from unittest.mock import patch

from app.scorer import analyze_image
from app.models import AnalysisResult

VALID_RESPONSE = json.dumps({
    "overall_score": 7.5,
    "categories": {
        "contrast": {"score": 7, "note": "ok"},
        "spacing": {"score": 8, "note": "ok"},
        "hierarchy": {"score": 7, "note": "ok"},
        "alignment": {"score": 8, "note": "ok"},
        "color_harmony": {"score": 7, "note": "ok"},
    },
    "issues": [
        {"label": "test issue", "x": 0.1, "y": 0.1, "w": 0.2, "h": 0.2, "fix": "fix it"}
    ],
})

MALFORMED_RESPONSE = "not valid json at all"


def test_analyze_image_parses_valid_response():
    with patch("app.scorer.call_llm", return_value=VALID_RESPONSE):
        result = analyze_image("fake_base64_image")
        assert isinstance(result, AnalysisResult)
        assert result.overall_score == 7.5
        assert len(result.issues) == 1
        assert result.categories.contrast.score == 7


def test_analyze_image_retries_then_raises_on_persistent_malformed_response():
    with patch("app.scorer.call_llm", return_value=MALFORMED_RESPONSE) as mock_call:
        with pytest.raises(ValueError):
            analyze_image("fake_base64_image")
        # called twice: initial attempt + one retry
        assert mock_call.call_count == 2


def test_analyze_image_recovers_if_retry_succeeds():
    with patch("app.scorer.call_llm", side_effect=[MALFORMED_RESPONSE, VALID_RESPONSE]):
        result = analyze_image("fake_base64_image")
        assert isinstance(result, AnalysisResult)
        assert result.overall_score == 7.5
