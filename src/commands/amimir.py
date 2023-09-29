import os
import random

from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

app: Application
handler: CommandHandler

def init(_app: Application) -> None:
    global app, handler, db
    app = _app
    handler = CommandHandler("amimir", command)
    app.add_handler(handler)

def deinit() -> None:
    app.remove_handler(handler)

async def command(update: Update, context: CallbackContext) -> None:
    with os.scandir("resources/amimir") as it:
        entry = random.choice(list(it))
        await update.effective_message.reply_photo(entry.path)
