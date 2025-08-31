import os
import json
import requests
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("perspective_api_key")
if not API_KEY:
    raise ValueError("❌ No PERSPECTIVE_API_KEY found in .env file")

# Perspective API endpoint
PERSPECTIVE_URL = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={API_KEY}"


def detect_bullying(text: str):
    """Detect toxicity with Perspective API using requests"""
    analyze_request = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}}
    }

    response = requests.post(PERSPECTIVE_URL, json=analyze_request)
    result = response.json()

    if "attributeScores" not in result:
        print("API error:", result)
        return False, 0.0, None

    score = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]

    if score > 0.5:  # threshold
        return True, score, "toxic"
    return False, score, None

def academic_bullying_check(text: str):
    """Check for custom academic bullying keywords"""
    keywords = [
        "you'll fail",
        "stupid project",
        "grade shaming",
        "excluded from group",
        "dumb kid"
    ]
    for kw in keywords:
        if kw.lower() in text.lower():
            return True
    return False
