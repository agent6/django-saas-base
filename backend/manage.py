#!/usr/bin/env python
import os
import sys
from pathlib import Path

import dotenv


def main():
    # Load .env file from the project root
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        dotenv.load_dotenv(env_path)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your "
            "PYTHONPATH environment variable?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
