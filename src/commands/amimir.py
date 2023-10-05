import os
import random
import sqlite3
import logging

from telegram import Update, Video, Animation
from telegram.ext import (
    Application,
    BaseHandler,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    filters,
)

# at least multi-thread mode
assert sqlite3.threadsafety >= 2

app: Application
handlers: list[BaseHandler]
db: sqlite3.Connection

def init(_app: Application) -> None:
    global app, handlers, db
    app = _app
    db = sqlite3.connect("resources/amimir.db", check_same_thread=False)
    create_table()

    handlers = [
        CommandHandler("amimir", amimir_command),
        MessageHandler(
            filters.ChatType.PRIVATE
            & (filters.PHOTO | filters.VIDEO | filters.ANIMATION),
            pm_handler,
        )
    ]
    app.add_handlers(handlers)

def deinit() -> None:
    for handler in handlers:
        app.remove_handler(handler)
    db.close()

def create_table() -> None:
    db.execute("""create table if not exists media
        ( id integer primary key not null
        , media_type text not null
        , tg_file_id text not null
        , tg_file_unique_id text unique not null
        , tg_user_id integer not null
        , timestamp datetime default current_timestamp not null
        )
    """)

async def amimir_command(update: Update, context: CallbackContext) -> None:
    (media_type, tg_file_id) = db.execute(
        # FIXME: slow when database becomes large
        "select media_type, tg_file_id from media order by random() limit 1",
    ).fetchone()

    match media_type:
        case "photo":
            await update.effective_message.reply_photo(tg_file_id)
        case "video":
            await update.effective_message.reply_video(tg_file_id)
        case "animation":
            await update.effective_message.reply_animation(tg_file_id)
        case _:
            raise Exception("invalid media type")

async def pm_handler(update: Update, context: CallbackContext) -> None:
    attachment = update.effective_message.effective_attachment
    match attachment:
        # FIXME: check the type inside the list
        case [*photos]:
            media_type = "photo"
            attachment = photos[-1]
        case Video():
            media_type = "video"
        case Animation():
            media_type = "animation"
        case _:
            raise Exception("invalid attachment")

    tg_file_id = attachment.file_id
    tg_file_unique_id = attachment.file_unique_id
    tg_user_id = update.effective_user.id

    translation = {"photo": "Photo", "video": "Vidéo", "animation": "Animation"}
    try:
        with db:
            db.execute(
                "insert into media (media_type, tg_file_id, tg_file_unique_id, tg_user_id) values (?, ?, ?, ?)",
                (media_type, tg_file_id, tg_file_unique_id, tg_user_id),
            )
    except sqlite3.IntegrityError as exc:
        logging.exception(f"exception while adding amimir {media_type}:", exc_info=exc)
        await update.effective_message.reply_text(f"{translation[media_type]} déjà présente dans la base de données")
    except Exception as exc:
        logging.exception(f"exception while adding amimir {media_type}:", exc_info=exc)
        await update.effective_message.reply_text(f"{translation[media_type]} non ajoutée, il y a eu une erreur")
    else:
        await update.effective_message.reply_text(f"{translation[media_type]} ajoutée, merci !")
