import logging
import importlib
import os
import sys

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, CallbackContext
from typing import Union
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, FileClosedEvent, FileDeletedEvent

class CommandFileHandler(PatternMatchingEventHandler):
    app: Application

    def __init__(self, app: Application) -> None:
        super().__init__(
            patterns=["*.py"],
            ignore_patterns=[".*"],
            ignore_directories=True,
        )
        self.app = app

    def on_closed(self, event: FileClosedEvent) -> None:
        # TODO: vs on_modified?
        (name, _) = os.path.splitext(os.path.basename(event.src_path))
        mod_name = f"commands.{name}"
        if mod_name in sys.modules:
            mod = sys.modules[mod_name]
            mod.deinit()
            logging.info(f"reloading module {mod_name}")
            try:
                importlib.reload(mod)
            except Exception as exc:
                logging.exception(f"exception while loading {mod_name}:", exc_info=exc)
                return
        else:
            logging.info(f"importing module {mod_name}")
            try:
                mod = importlib.import_module(mod_name)
            except Exception as exc:
                logging.exception(f"exception while loading {mod_name}:", exc_info=exc)
                return
        mod.init(self.app)

    def on_deleted(self, event: FileDeletedEvent) -> None:
        (name, _) = os.path.splitext(os.path.basename(event.src_path))
        mod_name = f"commands.{name}"
        sys.modules[mod_name].deinit()
        del sys.modules[mod_name]

def main():
    logging.basicConfig(level=logging.INFO)
    load_dotenv()

    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    with os.scandir("src/commands") as it:
        for entry in it:
            if not entry.is_file():
                continue
            match entry.name.rsplit(sep=".", maxsplit=1):
                case [name, "py"] if name[0] != ".":
                    mod_name = f"commands.{name}"
                    logging.info(f"importing module {mod_name}")
                    mod = importlib.import_module(mod_name)
                    mod.init(app)

    event_handler = CommandFileHandler(app)
    observer = Observer()
    observer.schedule(event_handler, "src/commands")
    observer.start()

    app.run_polling()

if __name__ == "__main__":
    main()
