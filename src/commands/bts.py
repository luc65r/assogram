import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = os.getenv("BTS_SPREADSHEET_ID")
RANGE = os.getenv("BTS_RANGE")
LINK = os.getenv("BTS_LINK")

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

    handler = CommandHandler("bts", command)
    app.add_handler(handler)

def deinit() -> None:
    app.remove_handler(handler)

async def command(update: Update, context: CallbackContext) -> None:
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
    [taken, remaining_bus, remaining_party] = result["values"][0]
    await update.effective_message.reply_html(f"""<b>Soirée Back To School</b>
    Lien d'inscription : {LINK}
    Il reste {remaining_party} places, dont {remaining_bus} pour le bus de 23h.
    Vous avez jusqu'au vendredi 6 octobre à 21h pour vous inscrire.
    """)
