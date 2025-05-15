from telegram import Update
from telegram.ext import ContextTypes
from Data_Base.database import db
from Admin.send_large_message import send_large_message

#Получение списка тестов
async def get_tests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        requester = update.effective_user.username
        if not db.is_admin(requester):
            await update.effective_message.reply_text("⛔ У вас нет доступа к этой команде.")
            return

        tests = db.get_tests()

        if not tests:
            await update.effective_message.reply_text("❌ В базе данных нет тестов.")
            return

        message = "📋 Список тестов:\n\n"

        for i, test in enumerate(tests, 1):
            if 'discipline' not in test or 'course' not in test or 'topic' not in test or 'title' not in test or 'questions' not in test:
                message += f"⚠️ Ошибка в тесте {i}: отсутствуют необходимые данные.\n"
                print(f"Ошибка в тесте {i}: отсутствуют необходимые данные.")
                continue

            message += (
                f"{i}. 📘 Дисциплина: {test['discipline']}\n"
                f"   📗 Курс: {test['course']}\n"
                f"   📙 Тема: {test['topic']}\n"
                f"   📓 Урок: {test['title']}\n"
            )

            #Итерация по всем вопросам в тесте
            for j, question in enumerate(test["questions"], 1):

                if "type" not in question or "text" not in question:
                    message += f"⚠️ Ошибка в вопросе {j} теста {i}: отсутствуют тип или текст вопроса.\n"
                    continue

                message += f"   ❓ Вопрос {j}: {question['text']}\n"
                message += f"   🧪 Тип: {question['type']}\n"

                if question["type"] == "multiple_choice":
                    if "options" not in question or "correct_answer" not in question:
                        message += f"⚠️ Ошибка в вопросе {j} теста {i}: отсутствуют варианты ответа или правильный ответ.\n"
                        continue
                    options = "\n".join([f"      {idx+1}. {opt}" for idx, opt in enumerate(question["options"])])
                    message += f"     Варианты ответа:\n{options}\n"
                    correct_answer = question["correct_answer"]
                    message += f"   ✅ Правильный вариант: {question['options'][int(correct_answer)-1]}\n"

                elif question["type"] == "text_answer":
                    if "correct_answer" not in question:
                        message += f"⚠️ Ошибка в вопросе {j} теста {i}: отсутствует правильный ответ.\n"
                        continue
                    message += f"   ✅ Правильный ответ: {question['correct_answer']}\n"

                
            message += "\n\n"
        message += "\n\n"
        await send_large_message(update, message)

    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка при получении тестов: {str(e)}")
        print(f"Ошибка: {str(e)}")