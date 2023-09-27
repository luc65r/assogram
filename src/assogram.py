import logging
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from telegram.constants import ParseMode
from typing import Optional

class Handler:
    path: str
    parse_mode: str

    def __init__(self, path: str, filetype: str) -> None:
        self.path = path
        match filetype:
            case "md":
                self.parse_mode = ParseMode.MARKDOWN_V2
            case "html":
                self.parse_mode = ParseMode.HTML
            case _:
                raise ValueError(f"unknown file type: {filetype}")

    async def __call__(self, update: Update, context: CallbackContext) -> None:
        with open(self.path, "r") as f:
            text = f.read()
            await context.bot.send_message(
                update.effective_message.chat_id,
                text,
                parse_mode=self.parse_mode,
            )

def command_handler_factory(entry: os.DirEntry) -> Optional[CommandHandler]:
    if not entry.is_file():
        return None
    match entry.name.rsplit(sep=".", maxsplit=1):
        case [cmd_name, ("md" | "html") as filetype]:
            return CommandHandler(cmd_name, Handler(entry.path, filetype))
    return None

def main():
    logging.basicConfig(level=logging.INFO)

    app = ApplicationBuilder().token("").build()

    with os.scandir("commands") as it:
        for entry in it:
            ch = command_handler_factory(entry)
            if ch is not None:
                app.add_handler(ch)
                logging.info(f"added command handler for {ch.commands}")

    app.run_polling()

if __name__ == "__main__":
    main()
