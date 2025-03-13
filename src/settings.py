import os
from dotenv import load_dotenv
load_dotenv()
import logging


ID_INSTANCE = os.environ.get("ID_INSTANCE")
API_TOKEN_INSTANCE = os.environ.get("API_TOKEN_INSTANCE")
CRM_TOKEN = os.environ.get("CRM_TOKEN")
CRM_URL = os.environ.get("CRM_URL")

DEBUG = os.environ.get("DEBUG", "False") == "True"
if DEBUG:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO

OPERATOR_PHONE_NUMBER = os.environ.get("OPERATOR_PHONE_NUMBER")

YANDEX_CATALOG_ID = os.environ.get("YANDEX_CATALOG_ID")
YANDEX_API_TOKEN = os.environ.get("YANDEX_API_TOKEN")