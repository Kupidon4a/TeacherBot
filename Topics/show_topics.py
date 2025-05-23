from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from Data_Base.database import db
from User.user import user

async def show_topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        topics = db.get_topics(user.discipline, user.course)
        buttons = []
        for topic in topics:
            topic_id = str(abs(hash(topic)))[:8]
            buttons.append([InlineKeyboardButton(topic, callback_data=f"topic_{topic_id}")])
            context.user_data[f"topic_{topic_id}"] = topic
        
        buttons.append([InlineKeyboardButton("🔙 Назад", callback_data="back_to_courses")])
        
        await update.callback_query.message.reply_text(
            f"📚 Курс: <b>{user.course}</b>\nВыбери тему:",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Ошибка в show_topics: {str(e)}")
        await update.callback_query.message.reply_text("⚠️ Ошибка при загрузке тем")