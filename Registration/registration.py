from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler
)

import Data_Base.database as db
from validation import *
import asyncio



from User.user import user
from Menu.menu import *


ASK_FIRST_NAME, ASK_LAST_NAME, ASK_AGE, ASK_CITY = range(4)

async def check_user_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_1 = update.effective_user
    print(f"Логин пользователя: {user_1.username}")
    if user_1.username == None:
        await update.message.reply_text("Задайте логин в настройках приложения Telegram, после чего можете заново регистрироваться!!!", parse_mode="Markdown")
        return
    user.set_login(user_1.username)
    answer_db = db.db.is_user(user_1.username)
    if answer_db:
        print("Меню")
        await menu(update, context)
        return ConversationHandler.END
    else:
        print("Старт")
        await start(update, context)
        return ASK_FIRST_NAME


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_1 = update.effective_user
    user.set_login(user_1.username) 
    welcome_text = """
Привет! Я учебный бот.

Вместе со мной ты сможешь научиться новым для себя вещам 
и с легкостью освоить новые для себя технологии. 

Но для начала давай пройдем регистрацию. 

Для этого скорее заполняй данные о себе в диалоге ниже и мы сразу приступим к обучению.

Сразу напиши свое имя, после чего получишь дальнейшие инструкции
    """
    await update.message.reply_text(welcome_text, parse_mode="Markdown")


async def ask_first_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.message.text
    if not validate_name(user_first_name):
        await update.message.reply_text("Неверный формат. Пример: Александр")
        return ASK_FIRST_NAME
    user.set_first_name(user_first_name)
    await update.message.reply_text(f"Приятно познакомиться, {user.get_first_name()}! Также укажи пожалуйста свою фамилию:")
    return ASK_LAST_NAME

async def ask_last_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_last_name = update.message.text
    if not validate_name(user_last_name):
        await update.message.reply_text("Неверный формат. Пример: Петров")
        return ASK_LAST_NAME
    user.set_last_name(user_last_name)
    await update.message.reply_text(f"Спасибо, твоя фамилия {user.get_last_name()}! Укажи пожалуйста теперь свой возраст:")
    return ASK_AGE

def get_user_age_text(user_age):
    user_age_text = None
    if str(user_age)[-1] == '1':
        user_age_text = 'год'

    elif str(user_age)[-1] == '2' or str(user_age)[-1] == '3' or str(user_age)[-1] == '4':
        user_age_text = 'года'

    else:
        user_age_text = 'лет'
    return user_age_text

async def ask_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_age = update.message.text
    if not validate_age(user_age):
        await update.message.reply_text("Возраст должен быть целым числом от 1 до 120")
        return ASK_AGE
    user.set_age(user_age)
    user_age_text = get_user_age_text(user_age)
    await update.message.reply_text(

        f"Ты {user.get_first_name()} {user.get_last_name()}, тебе {user.get_age()} {user_age_text}. Теперь укажи пожалуйста город своего проживания:"
    )
    return ASK_CITY

async def ask_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_city = update.message.text
    if not validate_city(user_city):
        await update.message.reply_text("Неверный формат. Пример: Москва")
        return ASK_CITY
    user.set_city(user_city)
    await update.message.reply_text(f"Ты {user.get_first_name()} {user.get_last_name()}, тебе {user.get_age()} {get_user_age_text(user.get_age())}. Ты проживаешь в городе {user.get_city()}")
    print(user_city)
    db.db.add_user(user.get_first_name(), user.get_last_name(), user.get_age(), user.get_city(), user.get_login())
    

    
    await asyncio.sleep(2)
    text = f"""Приятно познакомиться, мой дорогой друг {user.get_first_name()} {user.get_last_name()}!

Я рад, что ты пришел учиться одной из самых высокооплачиваемых и востребованных специальностей.

Чтобы начать обучение, нажми на кнопку "Хочу учиться" """
    await update.message.reply_text(text, parse_mode="Markdown")
    await menu(update, context)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Диалог прерван.")
    return ConversationHandler.END