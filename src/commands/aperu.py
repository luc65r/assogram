from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

app: Application
handler: CommandHandler

def init(_app: Application) -> None:
    global app, handler
    app = _app
    handler = CommandHandler("aperu", command)
    app.add_handler(handler)

def deinit() -> None:
    app.remove_handler(handler)

async def command(update: Update, context: CallbackContext) -> None:
    await update.effective_message.reply_venue(
        latitude=43.3168795,
        longitude=-0.3642176,
        title="L'Apéru",
        address="Rue Saint-John Parse, 64000 Pau",
        google_place_id="ChIJDbvVyv9JVg0REQ4SMlXrqIo",
        google_place_type="bar",
    )
