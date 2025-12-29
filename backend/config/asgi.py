import os
from pathlib import Path

import dotenv
from django.core.asgi import get_asgi_application

# Load .env file from the project root
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
if env_path.exists():
    dotenv.load_dotenv(env_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()
