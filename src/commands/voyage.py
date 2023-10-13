import os
from datetime import datetime, timedelta

import humanize
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram.constants import ParseMode

app: Application
handler: CommandHandler

def init(_app: Application) -> None:
    global app, handler
    app = _app

    handler = CommandHandler("voyage", command)
    app.add_handler(handler)

def deinit() -> None:
    app.remove_handler(handler)

async def command(update: Update, context: CallbackContext) -> None:
    await update.effective_message.reply_photo("resources/voyage_annulé.jpg")
    
