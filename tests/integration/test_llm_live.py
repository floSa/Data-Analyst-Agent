"""Test live du LLM réel (serveur local) — exclu par défaut et en CI.

Lancer explicitement : uv run pytest -m live --no-cov
"""

import pytest

from data_analyst_agent.config import Settings
from data_analyst_agent.llm import build_model

pytestmark = pytest.mark.live


def test_ping_de_bout_en_bout():
    from pydantic_ai import Agent

    agent = Agent(
        # La suite coupe le `.env` du poste (tests/conftest.py) : un test live
        # le relit explicitement, pour viser le service central avec sa clé.
        build_model(Settings(_env_file=".env")),
        system_prompt="Réponds au message par le seul mot : pong",
    )
    result = agent.run_sync("ping")
    assert "pong" in result.output.lower()
