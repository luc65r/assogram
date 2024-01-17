import os
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import humanize
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram.constants import ParseMode

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = os.getenv("NEON_SPREADSHEET_ID")
RANGE = os.getenv("NEON_RANGE")
LINK = os.getenv("NEON_LINK")

app: Application
handler: CommandHandler

def init(_app: Application) -> None:
    global app, handler, sheet
    app = _app

    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    humanize.i18n.activate("fr_FR")

    handler = CommandHandler("neon", command)
    app.add_handler(handler)

def deinit() -> None:
    app.remove_handler(handler)

async def command(update: Update, context: CallbackContext) -> None:
    delta = datetime(2024, 01, 26, 22, 00) - datetime.now()
    if update.effective_user is not None and update.effective_user.first_name == "Yan":
        await update.effective_message.reply_photo("resources/yan_neon.jpg")
    elif delta >= timedelta(0):
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
        remaining = result["values"][0][0]
        remaining_time = humanize.precisedelta(delta, minimum_unit="seconds", format="%0.0f")
        await update.effective_message.reply_photo(
            "resources/affiche_neon_party.jpg",
            caption=f"""<b>Neon Party</b>
Lien d'inscription : {LINK} (ferme dans {remaining_time}).
Il reste {remaining} places.""",
            parse_mode=ParseMode.HTML,
        )
    else:
        await update.effective_message.reply_photo("resources/dembele.jpg")
