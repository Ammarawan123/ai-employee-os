"""
Phase 5a: Config
--------------------
Central place for API keys / provider config. Add keys to your .env as you
get them - nothing breaks if a key is missing, the router just skips that
provider and falls back to the local model (see llm_router.py).
"""

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def available_providers() -> list[str]:
    """Which remote providers actually have a key configured right now."""
    providers = ["local"]  # local model is always available - no key needed
    if OPENAI_API_KEY:
        providers.append("openai")
    if ANTHROPIC_API_KEY:
        providers.append("anthropic")
    if GEMINI_API_KEY:
        providers.append("gemini")
    return providers