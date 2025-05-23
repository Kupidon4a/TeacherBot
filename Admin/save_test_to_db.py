from telegram import Update
from telegram.ext import ContextTypes
from Data_Base.database import db

    

async def save_test_to_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
    test_data = context.user_data["add_test"]
    q = test_data["question"]
    db.add_test(test_data["discipline"], test_data["course"], test_data["topic"], test_data['lesson'], q['type'], q['text'], q['correct'], q.get('options'))