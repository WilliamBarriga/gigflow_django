import os
from typing import Any
from dotenv import main
from pathlib import Path

env_path = Path(".") / ".env"
main.load_dotenv()


def load_env(prop: str, cast: type = str) -> Any:
    """Load environment variable and cast it to the specified type."""
    env = os.getenv(prop)
    if cast == bool:
        env = True if env.lower == "true" else False
    return cast(env)
