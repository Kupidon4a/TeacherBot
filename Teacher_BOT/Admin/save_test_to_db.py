from telegram import Update
from telegram.ext import ContextTypes
from Data_Base.database import db

    

async def save_test_to_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
    test_data = context.user_data["add_test"]
    q = test_data["question"]
    print("🧪 Сохраняем в БД:")
    print(f"Дисциплина: {test_data["discipline"]}")
    print(f"Курс: {test_data["course"]}")
    print(f"Тема: {test_data["topic"]}")
    print(f"Урок: {test_data['lesson']}")
    print(f"Тип: {q['type']}")
    print(f"Текст: {q['text']}")
    print(f"Ответ: {q['correct']}")
    print(f"Варианты: {q.get('options')}")

    db.add_test(test_data["discipline"], test_data["course"], test_data["topic"], test_data['lesson'], q['type'], q['text'], q['correct'], q.get('options'))