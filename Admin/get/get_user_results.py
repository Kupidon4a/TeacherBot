from telegram import Update, InputFile
from telegram.ext import ContextTypes
from Data_Base.database import db

import csv
import io

    
#Выгрузка результатов тестирования в CSV файл
async def get_all_user_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    requester = update.effective_user.username
    if not db.is_admin(requester):
        await update.effective_message.reply_text("⛔ У вас нет доступа к этой команде.")
        return
    
    
    results = await db.get_all_results()

    if not results:
        await update.message.reply_text("Результаты отсутствуют.")
        return

    text_stream = io.StringIO()
    text_stream.write('\ufeff')
    writer = csv.writer(text_stream, delimiter=";")

    writer.writerow([
        "Логин телеграм", "Дисциплина", "Курс", "Тема", "Урок",
        "Вопрос", "Ответ пользователя", "Правильный ответ", "Правильность ответа пользователя"
    ])

    for r in results:
        writer.writerow([
            r.get("login", ""),
            r.get("discipline", ""),
            r.get("course", ""),
            r.get("topic", ""),
            r.get("title", ""),
            r.get("question", ""),
            r.get("user_answer", ""),
            r.get("correct_answer", ""),
            "1" if r.get("is_correct") else "0"
        ])

    byte_stream = io.BytesIO(text_stream.getvalue().encode('utf-8-sig'))
    byte_stream.seek(0)

    file = InputFile(byte_stream, filename="all_results.csv")
    await update.message.reply_document(file, caption="📊 Результаты всех пользователей")