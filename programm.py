import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, MUZ, BIO = range(5)
def start(update, _):
    reply_keyboard = [['Boy', 'Girl', 'Other']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        'Такси-Бот приветствует тебя! Ответь на несколько вопросов, чтобы заказать такси. '
        'Команда /cancel, чтобы прекратить разговор.\n\n'
        'Предпочитаешь водителя мужчину или женщину?',
        reply_markup=markup_key,)
    
    return GENDER

def gender(update, _):
    user = update.message.from_user
    logger.info("Пол водителя %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Хорошо. Пришли мне свою фотографию, чтоб я узнал тебя '
        'в толпе прохожих, или отправь /skip, если стесняешься.',
        reply_markup=ReplyKeyboardRemove(),
    )
    return PHOTO

def photo(update, _):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file() 
    photo_file.download(f'{user.first_name}_photo.jpg')
    logger.info("Фотография %s: %s", user.first_name, f'{user.first_name}_photo.jpg')
    update.message.reply_text(
        'Великолепно! А теперь пришли мне свое'
        ' местоположение, или /skip если не хочешь, чтобы за тобой приезжали'
    )
    return LOCATION

def skip_photo(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s не отправил фото.", user.first_name)
    update.message.reply_text(
        'Держу пари, ты выглядишь великолепно! А теперь пришлите мне'
        ' свое местоположение, или /skip если не хочешь, чтобы за тобой приезжали'
    )
    return LOCATION

def location(update, _):
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Местоположение %s: %s / %s", user.first_name, user_location.latitude, user_location.longitude)
    update.message.reply_text(
        'Отлично. Водитель уже едет к тебе!' 
        'Расскажи мне какую музыку предпочитаешь?'
    )
    return MUZ

def skip_location(update, _):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text(
        'Раз не хочешь вызывать такси, тогда расскажи мне что-нибудь о себе...'
    )
    return BIO

def muz(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s рассказал: %s", user.first_name, update.message.text)
    update.message.reply_text('Спасибо! Водитель уже поставил твою любимую пластинку.'
                              'Ожидай, скоро будет на месте.')
    return ConversationHandler.END

def bio(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s рассказал: %s", user.first_name, update.message.text)
    update.message.reply_text('Спасибо! Надеюсь, когда-нибудь снова сможем поговорить.')
    return ConversationHandler.END

def cancel(update, _):
    user = update.message.from_user
    logger.info("Пользователь %s отменил вызов.", user.first_name)
    update.message.reply_text(
        'Мое дело предложить - Ваше отказаться'
        'Понадобится машина - пиши.', 
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END