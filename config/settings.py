"""
Configuration settings for the hackathon project.

This file contains default settings. You can override these by creating
a local_config.py file in the same directory (which is gitignored).
"""

# Application settings
APP_NAME = "Hackathon Project"
VERSION = "1.0.0"
DEBUG = True

# Database settings (example)
DATABASE_URL = "sqlite:///hackathon.db"

# API settings (example)
API_BASE_URL = "https://api.example.com"
API_TIMEOUT = 30

# Logging settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Try to import local configuration overrides
try:
    from .local_config import *  # noqa: F401, F403
except ImportError:
    pass
