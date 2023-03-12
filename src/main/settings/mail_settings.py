from pathlib import Path
from dotenv import load_dotenv
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PARENT_DIR = Path(__file__).resolve().parent.parent.parent.parent

env_path = PARENT_DIR / "auth/.env"
load_dotenv(env_path)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.environ.get("EMAIL_PORT") #メールサーバーで指定されているポート
EMAIL_USE_TLS = True #メールサーバーで確認（TSLの場合もある）
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")