import logging
import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

TOKEN = "8825073734:AAE7Wo2rdUh40mhaf-8LWaR9gm0pivSRipM"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

NAME, LEVEL = range(2)
user_data = {}

def get_main_keyboard():
    keyboard = [
        [KeyboardButton("🏋️ Тренировка"), KeyboardButton("🏃‍♂️ Пробежка")],
        [KeyboardButton("📊 Статистика"), KeyboardButton("🎮 Мой уровень")],
        [KeyboardButton("⚙️ Настроить нагрузку"), KeyboardButton("ℹ️ Помощь")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_data:
        user_data[user_id] = {'name': '', 'level': 1, 'xp': 0, 'trainings': 0}
        await update.message.reply_text(
            "Приветствую, атлет! Я — твой тренер в кармане. Как мне тебя называть? (Напиши своё имя)",
            reply_markup=ReplyKeyboardMarkup([["Отмена"]], resize_keyboard=True)
        )
        return NAME
    else:
        name = user_data[user_id].get('name', 'атлет')
        await update.message.reply_text(
            f"С возвращением, {name}! Выбери действие:",
            reply_markup=get_main_keyboard()
        )
        return ConversationHandler.END

async def set_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    name = update.message.text
    user_data[user_id]['name'] = name
    await update.message.reply_text(
        f"Отлично, {name}! Теперь ты часть FITBRO. Выбери действие:",
        reply_markup=get_main_keyboard()
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Хорошо, давай начнём заново. Напиши /start")
    return ConversationHandler.END

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    user = user_data.get(user_id)
    if not user:
        await update.message.reply_text("Напиши /start, чтобы начать.")
        return

    if text == "🏋️ Тренировка":
        exercises = [
            "Приседания: 3 подхода × 15 раз",
            "Отжимания: 3 подхода × 12 раз",
            "Выпады: 3 подхода × 12 раз на каждую ногу",
            "Планка: 3 подхода по 30 секунд",
            "Подъём ног лёжа: 3 подхода × 15 раз",
            "Скручивания: 3 подхода × 20 раз",
            "Бёрпи: 3 подхода × 10 раз",
            "Альпинист: 3 подхода по 20 секунд"
        ]
        workout = random.sample(exercises, 5)
        plan = "\n".join(workout)
        await update.message.reply_text(
            f"🔥 Твоя тренировка на сегодня:\n\n{plan}\n\nВыполни все упражнения и нажми 'Готово'.",
            reply_markup=ReplyKeyboardMarkup([["✅ Готово"], ["🔙 Назад в меню"]], resize_keyboard=True)
        )

    elif text == "🏃‍♂️ Пробежка":
        await update.message.reply_text(
            "🏃‍♂️ Сегодня — пробежка. Беги в разговорном темпе (пульс до 140).\nТвоя дистанция: 1 км (по умолчанию).\nКогда закончишь — нажми 'Готово'.",
            reply_markup=ReplyKeyboardMarkup([["✅ Готово"], ["🔙 Назад в меню"]], resize_keyboard=True)
        )

    elif text == "📊 Статистика":
        stats = (
            f"📊 Твоя статистика:\n"
            f"👤 Имя: {user.get('name', 'Не указано')}\n"
            f"🏅 Уровень: {user['level']}\n"
            f"⭐ XP: {user['xp']}\n"
            f"🏋️ Тренировок: {user['trainings']}"
        )
        await update.message.reply_text(stats, reply_markup=get_main_keyboard())

    elif text == "🎮 Мой уровень":
        level = user['level']
        if level == 1:
            title = "Новичок"
        elif level == 2:
            title = "Исследователь"
        elif level == 3:
            title = "Боец"
        elif level == 4:
            title = "Атлет"
        elif level == 5:
            title = "Ветеран"
        else:
            title = "Мастер"
        await update.message.reply_text(
            f"🎮 Твой уровень: {level} - {title}\n⭐ XP: {user['xp']} / {level * 100 + 50}\nПродолжай тренироваться, чтобы повышать уровень!",
            reply_markup=get_main_keyboard()
        )

    elif text == "⚙️ Настроить нагрузку":
        await update.message.reply_text(
            "⚙️ Настройка нагрузки пока в разработке. Скоро здесь можно будет менять количество повторений и подходов!",
            reply_markup=get_main_keyboard()
        )

    elif text == "ℹ️ Помощь":
        await update.message.reply_text(
            "FITBRO — твой персональный тренер в кармане.\nТренируйся, повышай уровень, следи за статистикой.\nЕсли есть вопросы — пиши @Gleb_0707",
            reply_markup=get_main_keyboard()
        )

    elif text == "✅ Готово":
        user['xp'] += 15
        user['trainings'] += 1
        while user['xp'] >= user['level'] * 100 + 50:
            user['level'] += 1
        await update.message.reply_text(
            f"🔥 Отличная работа! Ты получил +15 XP.\nТеперь у тебя {user['xp']} XP.\n🏅 Уровень: {user['level']}\n\nНе забудь сделать растяжку!",
            reply_markup=get_main_keyboard()
        )

    elif text == "🔙 Назад в меню":
        await update.message.reply_text(
            "Возвращаю в главное меню.",
            reply_markup=get_main_keyboard()
        )

    else:
        await update.message.reply_text(
            "Я тебя не понял. Используй кнопки меню.",
            reply_markup=get_main_keyboard()
        )

def main():
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_name)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    print("🚀 Бот запущен и готов к работе! Нажми Ctrl+C для остановки.")
    application.run_polling()

if __name__ == "__main__":
    main()