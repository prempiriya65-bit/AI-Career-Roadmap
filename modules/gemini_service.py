"""
Gemini Service Module
Manages Google Gemini API initialization, model fallback, structured JSON prompting,
and robust error handling using the official `google-genai` SDK.
"""

import json
import os
import re
import streamlit as st
from typing import Dict, Any, Tuple, Optional

try:
    from google import genai
    from google.genai import types
    from google.genai import errors
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


# Supported and verified Gemini models in order of preference
PRIMARY_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash"
]


def get_api_key() -> str:
    """
    Retrieve Gemini API key with priority:
    1. Streamlit Session State (entered in UI setup modal/sidebar)
    2. Streamlit Secrets (.streamlit/secrets.toml)
    3. OS Environment Variable (GEMINI_API_KEY or GOOGLE_API_KEY)
    """
    # 1. Session state override
    if "custom_gemini_api_key" in st.session_state and st.session_state["custom_gemini_api_key"].strip():
        return st.session_state["custom_gemini_api_key"].strip()

    # 2. Streamlit secrets
    try:
        if "GEMINI_API_KEY" in st.secrets and str(st.secrets["GEMINI_API_KEY"]).strip():
            key = str(st.secrets["GEMINI_API_KEY"]).strip()
            if key != "YOUR_GEMINI_API_KEY" and key != "YOUR_API_KEY":
                return key
    except Exception:
        pass

    # 3. Environment variables
    env_key = os.environ.get("GEMINI_API_KEY", "").strip() or os.environ.get("GOOGLE_API_KEY", "").strip()
    if env_key and env_key != "YOUR_GEMINI_API_KEY":
        return env_key

    return ""


def is_api_configured() -> bool:
    """Check if a valid non-empty API key is available."""
    key = get_api_key()
    return bool(key and len(key) > 10)


def get_gemini_client(api_key: Optional[str] = None) -> Optional[Any]:
    """
    Create a google-genai Client instance.
    Returns None if SDK is not installed or API key is absent.
    """
    if not GENAI_AVAILABLE:
        return None

    key = api_key or get_api_key()
    if not key:
        return None

    try:
        client = genai.Client(api_key=key)
        return client
    except Exception as e:
        st.session_state["last_api_error"] = str(e)
        return None


def clean_json_text(raw_text: str) -> str:
    """Extract and sanitize JSON from model output."""
    text = raw_text.strip()
    # Strip markdown code blocks if present
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        text = match.group(1).strip()
    return text


def test_api_connection(api_key: Optional[str] = None) -> Tuple[bool, str]:
    """
    Verify API key connection with a minimal generation test.
    """
    key = api_key or get_api_key()
    if not key:
        return False, "API key is missing. Please configure GEMINI_API_KEY in .streamlit/secrets.toml"

    client = get_gemini_client(key)
    if not client:
        return False, "Could not initialize Google GenAI client."

    for model_name in PRIMARY_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents="Ping. Respond with single word 'OK'.",
                config=types.GenerateContentConfig(
                    max_output_tokens=10,
                    temperature=0.1
                )
            )
            if response and response.text:
                return True, f"Connected successfully using model: {model_name}"
        except errors.APIError as e:
            # Check for quota or auth errors
            if "API_KEY_INVALID" in str(e) or "400" in str(e):
                return False, f"Invalid API Key: {e.message if hasattr(e, 'message') else str(e)}"
            elif "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                return False, "Gemini API Quota Limit exceeded. Please check your billing or rate limits."
            continue
        except Exception as e:
            continue

    return False, "Failed to connect to Gemini API with available models. Please verify network access and API key."


def generate_structured_json(
    prompt: str,
    system_instruction: Optional[str] = None,
    preferred_model: Optional[str] = None
) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """
    Generate structured JSON response using Gemini API with automatic model fallback.
    Returns: (success, parsed_dict, error_message)
    """
    if not is_api_configured():
        return False, None, "Gemini API key is not configured. Please add GEMINI_API_KEY in .streamlit/secrets.toml"

    client = get_gemini_client()
    if not client:
        return False, None, "Google GenAI SDK client could not be initialized."

    models_to_try = [preferred_model] if preferred_model else []
    for m in PRIMARY_MODELS:
        if m not in models_to_try:
            models_to_try.append(m)

    last_error = "Unknown error"

    for model_name in models_to_try:
        try:
            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.3,
            )
            if system_instruction:
                config.system_instruction = system_instruction

            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config
            )

            if not response or not response.text:
                last_error = f"Model {model_name} returned an empty response."
                continue

            cleaned = clean_json_text(response.text)
            try:
                parsed = json.loads(cleaned)
                return True, parsed, None
            except json.JSONDecodeError as jde:
                last_error = f"Failed to parse JSON response from {model_name}: {str(jde)}"
                continue

        except errors.APIError as api_err:
            err_str = str(api_err)
            if "API_KEY_INVALID" in err_str or "unregistered" in err_str:
                return False, None, "Invalid Gemini API Key. Please provide a valid key from Google AI Studio."
            elif "RESOURCE_EXHAUSTED" in err_str or "429" in err_str:
                last_error = f"Model {model_name} quota exceeded (HTTP 429). Trying fallback model..."
                continue
            else:
                last_error = f"Gemini API Error ({model_name}): {err_str}"
                continue
        except Exception as ex:
            last_error = f"Error with model {model_name}: {str(ex)}"
            continue

    return False, None, f"All Gemini models failed. Last error: {last_error}"
