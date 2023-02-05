import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)

from programm import*
from config import TOKEN

if __name__ == '__main__':
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GENDER: [MessageHandler(filters.regex('^(Boy|Girl|Other)$'), gender)],
            PHOTO: [MessageHandler(filters.photo, photo), CommandHandler('skip', skip_photo)],
            LOCATION: [
                MessageHandler(filters.location, location),
                CommandHandler('skip', skip_location),
            ],
            BIO: [MessageHandler(filters.text & ~filters.command, bio)],
            MUZ: [MessageHandler(filters.text & ~filters.command, muz)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()