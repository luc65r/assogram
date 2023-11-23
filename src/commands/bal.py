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
SPREADSHEET_ID = os.getenv("BAL_SPREADSHEET_ID")
RANGE = os.getenv("BAL_RANGE")
LINK = os.getenv("BAL_LINK")

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

    handler = CommandHandler("bal", command)
    app.add_handler(handler)

def deinit() -> None:
    app.remove_handler(handler)

async def command(update: Update, context: CallbackContext) -> None:
    delta = datetime(2023, 12, 1, 21, 0) - datetime.now()
    if delta >= timedelta(0):
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
        [remaining_repas, remaining_soiree] = result["values"][0]
        remaining_time = humanize.precisedelta(delta, minimum_unit="seconds", format="%0.0f")
        await update.effective_message.reply_photo(
            "resources/affiche_bal_de_noel.jpg",
            caption=f"""<b>Bal de Noël</b>
Lien d'inscription : {LINK} ({remaining_time} restants).
Il reste {remaining_repas} places pour le repas, et {remaining_soiree} pour la soirée.""",
            parse_mode=ParseMode.HTML,
        )
    else:
        await update.effective_message.reply_photo("resources/dembele.jpg")
