import os
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import humanize
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram.constants import ParseMode

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = os.getenv("HALLOWEEN_SPREADSHEET_ID")
RANGE = os.getenv("HALLOWEEN_RANGE")
LINK = os.getenv("HALLOWEEN_LINK")

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

    handler = CommandHandler("halloween", command)
    app.add_handler(handler)

def deinit() -> None:
    app.remove_handler(handler)

async def command(update: Update, context: CallbackContext) -> None:
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
    remaining = result["values"][0][0]
    dl = datetime(2023, 11, 10, 21, 0)
    remaining_time = humanize.precisedelta(dl - datetime.now(), minimum_unit="seconds", format="%0.0f")
    await update.effective_message.reply_photo(
        "resources/affiche_halloween.jpg",
        caption=f"""<b>Soirée Halloween</b>
Lien d'inscription : {LINK}
Il reste {remaining} places.
Vous avez {remaining_time} (jusqu'au vendredi 10 novembre à 21h) pour vous inscrire.""",
        parse_mode=ParseMode.HTML,
    )
