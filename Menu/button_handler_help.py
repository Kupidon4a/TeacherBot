from telegram import Update
from telegram.ext import (
    ContextTypes
)
import asyncio
from Menu.menu import menu

async def button_handler_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'help_button_work':
        await query.message.reply_text(
            "Вы точно получите хорошую базу для изучения выбранной сферы. "
            "А если дополнительно тренироваться с нашим проектом, трудоустройство не за горами!"
        )
    elif query.data == 'help_button_question':
        await query.message.reply_text("@Ann_Ve поможет с любыми трудностями :)))")
    elif query.data == 'help_button_feedback':
        await query.message.reply_text("Оставьте отзыв здесь: [https://docs.google.com/forms/d/e/1FAIpQLScyERgR_ivF8_VwsvbTqjt9PWynDNEzX0Sm-njMWSKQr4mGXw/viewform]")
    elif query.data == 'help_button_survey':
        await query.message.reply_text(
            "Опрос нельзя пропустить — бот проверяет усвоение материала. "
            "Если есть трудности, напишите @Ann_Ve."
        )
    elif query.data == 'help_button_author':
        await query.message.reply_text(
            "Автор бота и курсов — Константин Брюханов, "
            "эксперт по DevOps и преподаватель ИТМО."
        )

    await asyncio.sleep(2)
    await menu(update, context)