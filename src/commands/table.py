from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

app: Application
handler: CommandHandler

def init(_app: Application) -> None:
    global app, handler
    app = _app
    handler = CommandHandler("table", command)
    app.add_handler(handler)

def deinit() -> None:
    app.remove_handler(handler)

async def command(update: Update, context: CallbackContext) -> None:
    await update.effective_message.reply_video("BAACAgQAAxkDAAMWZRR2trQuGBSPV0Cwo6JSBBjEDkUAApERAALl1KBQS3U0hOEqD-kwBA")
