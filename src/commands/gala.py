import os
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import humanize
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram.constants import ParseMode

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID_REPAS = os.getenv("GALA_SPREADSHEET_ID_REPAS")
SPREADSHEET_ID_SOIREE = os.getenv("GALA_SPREADSHEET_ID_SOIREE")
RANGE_REPAS = os.getenv("GALA_RANGE_REPAS")
RANGE_SOIREE = os.getenv("GALA_RANGE_SOIREE")
LINK_REPAS = os.getenv("GALA_LINK_REPAS")
LINK_SOIREE = os.getenv("GALA_LINK_SOIREE")

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

    handler = CommandHandler("gala", command)
    app.add_handler(handler)

def deinit() -> None:
    app.remove_handler(handler)

async def command(update: Update, context: CallbackContext) -> None:
    delta = datetime(2024, 3, 22, 20, 00) - datetime.now()
    if delta >= timedelta(0):
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID_REPAS, range=RANGE_REPAS).execute()
        remaining_repas = result["values"][0][0]
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID_SOIREE, range=RANGE_SOIREE).execute()
        remaining_soiree = result["values"][0][0]
        remaining_time = humanize.precisedelta(delta, minimum_unit="seconds", format="%0.0f")
        await update.effective_message.reply_media_group(
            [
                InputMediaPhoto("resources/affiche_gala.jpg"),
                InputMediaPhoto("resources/affiche_gala_repas.jpg"),
                InputMediaPhoto("resources/affiche_gala_soiree.jpg"),
            ],
            caption=f"""<b>Gala</b>
Inscription repas et soirée : {LINK_REPAS} ({remaining_repas} places restantes)
Inscription soirée uniquement : {LINK_SOIREE} ({remaining_soiree} places restantes)""",
            parse_mode=ParseMode.HTML,
        )
    else:
        await update.effective_message.reply_photo("resources/dembele.jpg")
