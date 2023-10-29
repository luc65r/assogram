import os
from datetime import datetime

import humanize
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

LINK = os.getenv("HALLOWEEN_LINK")

app: Application
handler: CommandHandler

def init(_app: Application) -> None:
    global app, handler
    app = _app

    humanize.i18n.activate("fr_FR")

    handler = CommandHandler("halloween", command)
    app.add_handler(handler)

def deinit() -> None:
    app.remove_handler(handler)

async def command(update: Update, context: CallbackContext) -> None:
    dl = datetime(2023, 11, 10, 21, 0)
    remaining_time = humanize.precisedelta(dl - datetime.now(), minimum_unit="seconds", format="%0.0f")
    await update.effective_message.reply_html(f"""<b>Soirée Halloween</b>
Lien d'inscription : {LINK}
Vous avez {remaining_time} (jusqu'au vendredi 10 novembre à 21h) pour vous inscrire.
    """)
