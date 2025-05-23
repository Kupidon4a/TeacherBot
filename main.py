from telegram.ext import (Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler
    )
from config import BOT_TOKEN
from admin import *

from Handlers.handler_teacher_discipline import handle_teacher_discipline
from Handlers.handler_course_selection import handle_course_selection
from Handlers.handler_topic_selection import handle_topic_selection
from Handlers.handler_text_answer import handle_text_answer
from Registration.registration import *
from Handlers.handle_lesson_selection import handle_lesson_selection

from Handlers.button_handler_menu import button_handler_menu
from Handlers.handle_back_buttons import handle_back_buttons
from Menu.button_handler_help import button_handler_help
from Lesson.show_lessons import show_lessons
from Handlers.handle_text_answers import handle_text_answers

from Stop.stop import stop

if __name__ == "__main__":
    
    #Создание бота
    app = Application.builder().token(BOT_TOKEN).build()

    #Модуль регистрации
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", check_user_db)],
        states={
            ASK_FIRST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_first_name)],
            ASK_LAST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_last_name)],
            ASK_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_age)],
            ASK_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_city)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    app.add_handler(conv_handler)

    #Основной функционал бота
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CallbackQueryHandler(button_handler_menu, pattern='^menu_button'))
    app.add_handler(CallbackQueryHandler(button_handler_help, pattern='^help_button'))
    app.add_handler(CallbackQueryHandler(handle_teacher_discipline, pattern="^teacher_"))
    app.add_handler(CallbackQueryHandler(handle_course_selection, pattern="^course_"))
    app.add_handler(CallbackQueryHandler(handle_topic_selection, pattern="^topic_"))
    app.add_handler(CallbackQueryHandler(handle_lesson_selection, pattern="^lesson_"))
    app.add_handler(CallbackQueryHandler(show_lessons, pattern="^show_lessons_"))
    app.add_handler(CallbackQueryHandler(handle_back_buttons, pattern="^back_"))
    #Основные обработчики для урока и теста
    app.add_handler(CallbackQueryHandler(handle_lesson_selection, pattern="^lesson_|^next_step$|^start_test$"))
    app.add_handler(CallbackQueryHandler(handle_text_answer, pattern="^answer_"))
    #Обработчик текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_answers))
 
    #Обработка всевозможных команд администратора
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("add_admin", add_admin))
    app.add_handler(CommandHandler("del_admin", del_admin))
    app.add_handler(CommandHandler("del_user", del_user))
    app.add_handler(CommandHandler("add_discipline", add_discipline))
    app.add_handler(CommandHandler("del_discipline", del_discipline))
    app.add_handler(CommandHandler("add_course", add_course))
    app.add_handler(CommandHandler("del_course", del_course))
    app.add_handler(CommandHandler("add_topic", add_topic))
    app.add_handler(CommandHandler("del_topic", del_topic))
    app.add_handler(CommandHandler("add_lesson", add_lesson))
    app.add_handler(CommandHandler("del_lesson", del_lesson))
    app.add_handler(CommandHandler("add_test", add_test))
    app.add_handler(CommandHandler("del_test", del_test))
    app.add_handler(CommandHandler("get_users", get_users))
    app.add_handler(CommandHandler("get_disciplines", get_disciplines))
    app.add_handler(CommandHandler("get_courses", get_courses))
    app.add_handler(CommandHandler("get_topics", get_topics))
    app.add_handler(CommandHandler("get_lessons", get_lessons))
    app.add_handler(CommandHandler("get_tests", get_tests))
    app.add_handler(CommandHandler("all_results", get_all_user_results))

    print("Бот запущен!")
    app.run_polling()