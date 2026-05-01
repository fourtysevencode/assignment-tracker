import json
import os
from urllib import error, request
from dotenv import load_dotenv

load_dotenv()


GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
ALLOWED_PRIORITIES = {"High", "Medium", "Low"}

# parse gemini respose
def _extract_json(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Gemini returned non-JSON output") from exc


def suggest_priority(assignment: str) -> dict:
    assignment_text = assignment.strip()
    if not assignment_text:
        raise ValueError("Assignment text is required")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set")

    prompt = (
        "You classify assignment urgency.\n"
        "Return ONLY JSON with keys: priority, reason.\n"
        'priority must be exactly one of: "High", "Medium", "Low".\n'
        "Keep reason under 20 words.\n"
        f"Assignment: {assignment_text}"
    )

    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        f"{GEMINI_ENDPOINT}?key={api_key}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

# handle outages and other gemini errors
    try:
        with request.urlopen(req, timeout=20) as resp:
            response_data = json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gemini API request failed: {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Could not reach Gemini API: {exc.reason}") from exc

    candidates = response_data.get("candidates", [])
    if not candidates:
        raise RuntimeError("Gemini response had no candidates")

    parts = candidates[0].get("content", {}).get("parts", [])
    if not parts or "text" not in parts[0]:
        raise RuntimeError("Gemini response did not include text output")

    parsed = _extract_json(parts[0]["text"])
    priority = parsed.get("priority")
    reason = parsed.get("reason")
    if priority not in ALLOWED_PRIORITIES:
        raise RuntimeError("Gemini returned invalid priority value")
    if not isinstance(reason, str) or not reason.strip():
        raise RuntimeError("Gemini returned an invalid reason")

    return {"priority": priority, "reason": reason.strip()}
