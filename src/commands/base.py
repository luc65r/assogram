from telegram import Update
from telegram.ext import (
    Application,
    BaseHandler,
    CommandHandler,
    CallbackContext,
)

app: Application
handlers: list[BaseHandler]

def init(_app: Application) -> None:
    global app, handlers
    app = _app
    handlers = [
        CommandHandler("start", start_command),
        CommandHandler("help", help_command),
    ]
    app.add_handlers(handlers)

def deinit() -> None:
    for handler in handlers:
        app.remove_handler(handler)

async def start_command(update: Update, context: CallbackContext) -> None:
    await update.effective_message.reply_text("""Bonjour !
Tu peux m'envoyer des photos/vidéos pour les ajouter à la commande amimir.
Contacte @luc65r si tu rencontres des problèmes.""")

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.effective_message.reply_html("""Commandes disponibles :
- <b>/help</b> Toute l'aide
- <b>/table</b> Éclate une table
- <b>/aperu</b> Appééérrrruuuuu
- <b>/amimir</b> Buenas noches uwu
- <b>/neon</b> Inscription Neon Party

Tu peux m'envoyer des photos/vidéos en message privé pour les ajouter à la commande amimir.
Contacte @luc65r si tu rencontres des problèmes.""")
