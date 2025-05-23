from telegram import Update
from telegram.ext import ContextTypes

from Handlers.handler_text_answer import handle_text_answer
from Admin.save_test_to_db import save_test_to_db
from Admin.handler_add_lesson import handler_add_lesson

async def handle_text_answers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('waiting_for_text_answer'):
        await handle_text_answer(update, context)
        return

    elif context.user_data.get("add_lesson_text"):
        await handler_add_lesson(update, context)
        return
    
    elif context.user_data.get("add_lesson_test"):
        test_data = context.user_data["add_test"]
        stage = test_data["stage"]
        
        msg = update.message.text.strip()
        if stage == "ask_question_text":
            test_data["question"]["text"] = msg
            test_data["stage"] = "ask_question_type"
            await update.message.reply_text("❓ Какой тип вопроса? Введите `multiple_choice` или `text_answer`:")
            return

        elif stage == "ask_question_type":
            if msg not in ("multiple_choice", "text_answer"):
                await update.message.reply_text("⚠️ Введите `multiple_choice` или `text_answer`.")
                return
            test_data["question"]["type"] = msg
            if msg == "multiple_choice":
                test_data["question"]["options"] = []
                test_data["stage"] = "collect_options"
                await update.message.reply_text("✅ Введите вариант ответа (введите `stop` когда закончите):")
            else:
                test_data["stage"] = "ask_correct_text"
                await update.message.reply_text("✅ Введите правильный ответ:")
            return

        elif stage == "collect_options":
            if msg.lower() == "stop":
                if len(test_data["question"]["options"]) < 2:
                    await update.message.reply_text("⚠️ Должно быть минимум два варианта.")
                    return
                test_data["stage"] = "ask_correct_option"
                options = "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(test_data["question"]["options"]))
                await update.message.reply_text(f"🟩 Введите номер правильного варианта:\n{options}")
                return
            test_data["question"]["options"].append(msg)
            await update.message.reply_text("➕ Добавлен. Введите следующий или `stop` для завершения:")
            return

        elif stage == "ask_correct_option":
            try:
                idx = int(msg) - 1
                if idx < 0 or idx >= len(test_data["question"]["options"]):
                    raise ValueError
                test_data["question"]["correct"] = idx
            except ValueError:
                await update.message.reply_text("⚠️ Введите корректный номер правильного варианта.")
                return

            await save_test_to_db(update, context)
            context.user_data["add_lesson_test"] = False
            await update.message.reply_text("✅ Вопрос добавлен. Хотите добавить еще? Воспользуйтесь командой /add_test заново!")
            context.user_data["add_test"]["question"] = {}
            context.user_data["add_test"]["stage"] = "ask_question_text"
            return

        elif stage == "ask_correct_text":
            test_data["question"]["correct"] = msg
            await save_test_to_db(update, context)
            context.user_data["add_lesson_test"] = False
            await update.message.reply_text("✅ Вопрос добавлен. Хотите добавить еще? Воспользуйтесь командой /add_test заново!")
            context.user_data["add_test"]["question"] = {}
            context.user_data["add_test"]["stage"] = "ask_question_text"
            return

        return

    else:
        await update.message.reply_text("⚠️ Сейчас не ожидается текстовый ответ. Пожалуйста, следуйте инструкциям.")
        return