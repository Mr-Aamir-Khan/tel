import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

PRICE_STARS = int(os.getenv("PRICE_STARS", "500"))

MEMBERSHIP_DAYS = int(
    os.getenv("MEMBERSHIP_DAYS", "30")
)

SUPPORT_USERNAME = os.getenv(
    "SUPPORT_USERNAME",
    ""
)

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing in .env")
