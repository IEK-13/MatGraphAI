from dotenv import load_dotenv
import os

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Mat2DevPlatform.settings")

from django.conf import settings
from django.core.management import execute_from_command_line

# Set up the Django environment
execute_from_command_line(["", "check"])

# Access settings
print(settings.OPENAI_API_KEY)
