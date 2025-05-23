
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)
import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Define states
NAME, PHONE, EXPERIENCE, TOOL, CAR, CITIZEN, HABITS, PHOTO, READY = range(9)

# Start handler with custom button
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("🚀 Подать анкету")]]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Привет! Мы набираем плиточников на заказы от Леруа Мерлен.\n\n"
        "Доход от 100 000 ₽/мес. Работа официальная, выплаты дважды в месяц.\n\n"
        "Жми кнопку ниже, если хочешь заполнить анкету!",
        reply_markup=markup,
    )
    return NAME

async def begin_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Как вас зовут?", reply_markup=ReplyKeyboardRemove())
    return PHONE

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Ваш номер телефона?")
    return EXPERIENCE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("Сколько лет укладываете плитку?")
    return TOOL

async def get_experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["experience"] = update.message.text
    await update.message.reply_text("Есть ли у вас инструмент? (Да/Нет)")
    return CAR

async def get_tool(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["tool"] = update.message.text
    await update.message.reply_text("Есть ли автомобиль? (Да/Нет)")
    return CITIZEN

async def get_car(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["car"] = update.message.text
    await update.message.reply_text("Есть ли гражданство РФ? (Да/Нет)")
    return HABITS

async def get_citizen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["citizen"] = update.message.text
    await update.message.reply_text("Есть ли вредные привычки? (курение, алкоголь, опоздания и т.д.)")
    return PHOTO

async def get_habits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["habits"] = update.message.text
    await update.message.reply_text("Прикрепите 1–2 фото ваших работ:")
    return READY

async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["photo"] = update.message.photo[-1].file_id if update.message.photo else "нет фото"
    await update.message.reply_text("Когда готовы выйти на первый объект?")
    return ConversationHandler.END

async def final_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ready"] = update.message.text

    user_info = "\n".join([f"{key}: {value}" for key, value in context.user_data.items()])
    await update.message.reply_text(f"Спасибо! Анкета получена:\n\n{user_info}\n\nМы с вами свяжемся. Вот мотивашка 👇")

    try:
        await update.message.reply_video_note(open("motivation.mp4", "rb"))
    except Exception as e:
        await update.message.reply_text("⚠️ Не удалось отправить видео: " + str(e))

    return ConversationHandler.END

# Run the bot
TOKEN = os.getenv("TELEGRAM_TOKEN")
app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", start),
        MessageHandler(filters.Regex("🚀 Подать анкету"), begin_form),
    ],
    states={
        NAME: [MessageHandler(filters.Regex("🚀 Подать анкету"), begin_form)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        EXPERIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        TOOL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_experience)],
        CAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_tool)],
        CITIZEN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_car)],
        HABITS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_citizen)],
        PHOTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_habits)],
        READY: [MessageHandler(filters.PHOTO | (filters.TEXT & ~filters.COMMAND), final_step)],
    },
    fallbacks=[],
)

app.add_handler(conv_handler)
app.run_polling()
