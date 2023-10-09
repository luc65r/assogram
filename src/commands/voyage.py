import os
from datetime import datetime, timedelta

import humanize
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram.constants import ParseMode

LINK = os.getenv("VOYAGE_LINK")

app: Application
handler: CommandHandler

def init(_app: Application) -> None:
    global app, handler
    app = _app

    humanize.i18n.activate("fr_FR")

    handler = CommandHandler("voyage", command)
    app.add_handler(handler)

def deinit() -> None:
    app.remove_handler(handler)

async def command(update: Update, context: CallbackContext) -> None:
    dl = datetime(2023, 10, 21)
    delta = dl - datetime.now()
    if delta >= timedelta(0):
        remaining_time = humanize.precisedelta(delta, minimum_unit="seconds", format="%0.0f")
        await update.effective_message.reply_photo(
            "resources/affiche_voyage.jpg",
            caption=f"""<b>Voyage en Espagne</b>
Plus que {remaining_time} pour prendre ta place à bord de la navette Paularis à destination de Salou !
Lien d'inscription : {LINK}""",
            parse_mode=ParseMode.HTML,
        )
    else:
        await update.effective_message.reply_photo("resources/dembele.jpg")
    
