
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

admin_chat_id = -4769038698  # Куда отправлять анкеты

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("🚀 Подать анкету")]]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        """👷‍♂️ Приветствуем!

Наша компания выполняет ремонты санузлов *под ключ* в Тюмени по заказам от Лемана Про (Леруа Мерлен).
Сейчас мы набираем опытных плиточников и мастеров отделки.

📋 *Что входит в работы:*
• Укладка плитки
• Демонтаж
• Подготовка стен и полов
• Установка сантехники
• Гидроизоляция, электрика, герметизация

💰 *Оплата:*
• Плитка — ~1600 ₽/м²
• Отдельно оплачиваются: демонтаж, затирка, порожки, сантехника и др.
• Аванс 20% — после завершения работ
• Основной платёж — в день выплат от Лемана Про
• Доход от 120 000 ₽/мес

📦 *Условия:*
• Работа по договору
• Спецодежда — выдаётся
• Инструмент — желательно свой (можем доукомплектовать)
• Стабильные заказы по Тюмени и пригородам

👇 Если всё устраивает — жми кнопку ниже и подай анкету. Это займёт не больше 2 минут.""",
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
    return READY

async def final_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ready"] = update.message.text

    user_info = (
        f"👤 Имя: {context.user_data.get('name')}
"
        f"📞 Телефон: {context.user_data.get('phone')}
"
        f"🛠️ Опыт: {context.user_data.get('experience')}
"
        f"🔧 Инструмент: {context.user_data.get('tool')}
"
        f"🚗 Авто: {context.user_data.get('car')}
"
        f"🇷🇺 Гражданство РФ: {context.user_data.get('citizen')}
"
        f"💭 Вредные привычки: {context.user_data.get('habits')}
"
        f"📆 Готовность выйти: {context.user_data.get('ready')}"
    )

    await update.message.reply_text(
        "✅ Спасибо, анкета отправлена!

"
        "Мы свяжемся с вами в течение 1–2 рабочих дней.
"
        "А пока — подготовьте инструмент, фото своих лучших работ и будьте на связи.

"
        "🟢 Лучшие мастера попадают в приоритетный список — не пропусти свой шанс 😉"
    )

    await context.bot.send_message(chat_id=admin_chat_id, text=f"📥 Новая анкета плиточника:

{user_info}")
    return ConversationHandler.END

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
app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, start))

app.run_polling()
