import io
from unittest.mock import patch

from fastapi.testclient import TestClient
from app.main import app
from app.models import AnalysisResult

client = TestClient(app)

MOCK_RESULT = AnalysisResult(**{
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


def test_root_returns_ok():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_returns_valid_result_for_valid_image():
    fake_image = io.BytesIO(b"fake image bytes")
    with patch("app.main.analyze_image", return_value=MOCK_RESULT):
        response = client.post(
            "/analyze",
            files={"file": ("test.png", fake_image, "image/png")},
        )
    assert response.status_code == 200
    body = response.json()
    assert body["overall_score"] == 7.5
    assert len(body["issues"]) == 1


def test_analyze_rejects_invalid_file_type():
    fake_file = io.BytesIO(b"not an image")
    response = client.post(
        "/analyze",
        files={"file": ("test.txt", fake_file, "text/plain")},
    )
    assert response.status_code == 400


def test_analyze_rejects_empty_file():
    fake_file = io.BytesIO(b"")
    response = client.post(
        "/analyze",
        files={"file": ("test.png", fake_file, "image/png")},
    )
    assert response.status_code == 400
