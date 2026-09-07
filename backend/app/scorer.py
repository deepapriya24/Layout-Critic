"""
Scoring logic for Layout Critic.

This module holds the prompt template and the call/parse/validate flow,
kept separate from route handling in main.py.

===========================================================================
 HOW TO PLUG IN A REAL LLM PROVIDER
===========================================================================
Right now `call_llm()` below returns a MOCK response so the rest of the
app (frontend, tests, CI) works with zero external dependencies or keys.

To wire up a real provider later:
  1. Add your provider's SDK to requirements.txt (openai / google-generativeai / anthropic)
  2. Set LLM_API_KEY in your .env file (see .env.example)
  3. Replace the body of call_llm() below with a real API call that:
       - sends `image_b64` and `PROMPT_TEMPLATE` to the provider
       - returns the raw text response (expected to be JSON matching
         the AnalysisResult schema in models.py)
  4. Leave everything else (validation, retry, error handling) as-is —
     it already expects a JSON string back from call_llm().
===========================================================================
"""

import os
import json
import random
from pydantic import ValidationError
from app.models import AnalysisResult

LLM_API_KEY = os.getenv("LLM_API_KEY", "")

PROMPT_TEMPLATE = """You are a senior UI/UX design critic. Analyze the attached UI screenshot
and return ONLY valid JSON (no markdown, no prose) in exactly this shape:

{
  "overall_score": <float 0-10>,
  "categories": {
    "contrast": {"score": <float 0-10>, "note": "<short note>"},
    "spacing": {"score": <float 0-10>, "note": "<short note>"},
    "hierarchy": {"score": <float 0-10>, "note": "<short note>"},
    "alignment": {"score": <float 0-10>, "note": "<short note>"},
    "color_harmony": {"score": <float 0-10>, "note": "<short note>"}
  },
  "issues": [
    {"label": "<issue label>", "x": <0-1>, "y": <0-1>, "w": <0-1>, "h": <0-1>, "fix": "<one-line fix>"}
  ]
}

x/y/w/h are normalized (0-1) bounding box coordinates relative to image dimensions.
"""


def _mock_llm_response() -> str:
    """
    Placeholder response generator. Returns randomized-but-plausible
    scores so the frontend has real-looking data to render during
    development, without needing any API key.
    """
    def cat(base_note):
        return {"score": round(random.uniform(5.5, 9.0), 1), "note": base_note}

    payload = {
        "overall_score": round(random.uniform(6.0, 8.5), 1),
        "categories": {
            "contrast": cat("Some text regions sit close to the WCAG minimum ratio."),
            "spacing": cat("Spacing is mostly consistent with a few tight clusters."),
            "hierarchy": cat("Primary action is identifiable but could be bolder."),
            "alignment": cat("Most elements align to a grid; minor drift on cards."),
            "color_harmony": cat("Palette is cohesive with one competing accent."),
        },
        "issues": [
            {
                "label": "Low contrast on subtitle text",
                "x": 0.12, "y": 0.22, "w": 0.35, "h": 0.06,
                "fix": "Increase contrast ratio to at least 4.5:1",
            },
            {
                "label": "Uneven spacing between cards",
                "x": 0.55, "y": 0.45, "w": 0.3, "h": 0.2,
                "fix": "Normalize gap to a consistent 16px/24px scale",
            },
            {
                "label": "CTA button lacks visual weight",
                "x": 0.4, "y": 0.75, "w": 0.2, "h": 0.08,
                "fix": "Increase size or use a higher-contrast fill color",
            },
        ],
    }
    return json.dumps(payload)


def call_llm(image_b64: str) -> str:
    """
    Sends the image + prompt to an LLM provider and returns the raw
    text response. Currently mocked — see module docstring for how to
    wire in a real provider.
    """
    # Real implementation would look roughly like:
    #   response = provider_client.generate(prompt=PROMPT_TEMPLATE, image=image_b64)
    #   return response.text
    return _mock_llm_response()


def analyze_image(image_b64: str) -> AnalysisResult:
    """
    Full flow: call the LLM, parse JSON, validate against the schema.
    Retries once with a stricter instruction if parsing/validation fails.
    Raises ValueError if it still fails after the retry.
    """
    raw = call_llm(image_b64)

    for attempt in range(2):
        try:
            data = json.loads(raw)
            return AnalysisResult(**data)
        except (json.JSONDecodeError, ValidationError) as exc:
            if attempt == 0:
                # Retry once — in a real provider integration this would
                # re-call the LLM with a stricter "JSON ONLY" instruction.
                raw = call_llm(image_b64)
                continue
            raise ValueError(f"Failed to parse/validate LLM response: {exc}") from exc
