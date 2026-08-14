import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.config import UNIVERSITY_INFO, ADMIN_IDS
from bot.keyboards import get_main_keyboard, get_back_keyboard, get_admin_keyboard
from bot.database import db

logger = logging.getLogger(__name__)

def is_admin(user_id):
    return user_id in ADMIN_IDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.add_user(user.id, user.username, user.first_name, user.last_name)
    welcome_text = (
        f"🎓 Добро пожаловать в {UNIVERSITY_INFO['name']}!\n\n"
        "Я помогу вам:\n"
        "• Связаться с приёмной комиссией\n"
        "• Найти нужный корпус\n"
        "• Узнать о факультетах\n"
        "• Получить информацию о поступлении\n\n"
        "Выберите нужный раздел:"
    )
    keyboard = get_main_keyboard()
    if is_admin(user.id):
        new_keyboard = [list(row) for row in keyboard.inline_keyboard]
        new_keyboard.append([InlineKeyboardButton("👨‍💻 Админ-панель", callback_data="admin")])
        keyboard = InlineKeyboardMarkup(new_keyboard)
    await update.message.reply_text(welcome_text, reply_markup=keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    data = query.data
    db.add_request(user.id, "button", data)

    if data == "contacts":
        response = get_contacts_text()
        await query.edit_message_text(response, reply_markup=get_back_keyboard(), parse_mode='HTML')
    elif data == "campuses":
        response = get_campuses_text()
        await query.edit_message_text(response, reply_markup=get_back_keyboard(), parse_mode='HTML')
    elif data == "admission":
        response = get_admission_text()
        await query.edit_message_text(response, reply_markup=get_back_keyboard(), parse_mode='HTML')
    elif data == "faculties":
        response = get_faculties_text()
        await query.edit_message_text(response, reply_markup=get_back_keyboard(), parse_mode='HTML')
    elif data == "branches":
        response = get_branches_text()
        await query.edit_message_text(response, reply_markup=get_back_keyboard(), parse_mode='HTML')
    elif data == "help":
        response = get_help_text()
        await query.edit_message_text(response, reply_markup=get_back_keyboard(), parse_mode='HTML')
    elif data == "admin":
        if is_admin(user.id):
            await query.edit_message_text("👨‍💻 Панель администратора:", reply_markup=get_admin_keyboard())
        else:
            await query.answer("⛔ У вас нет прав доступа!")
    elif data == "stats":
        if is_admin(user.id):
            await show_stats(query)
        else:
            await query.answer("⛔ У вас нет прав доступа!")
    elif data == "back":
        await start_callback(query)

async def show_stats(query):
    stats = db.get_user_stats()
    if not stats:
        await query.message.reply_text("❌ Не удалось получить статистику.")
        return
    response = "📊 <b>Статистика бота</b>\n\n"
    response += f"👥 Всего пользователей: <b>{stats['total_users']}</b>\n"
    response += f"📨 Всего запросов: <b>{stats['total_requests']}</b>\n\n"
    response += "📈 <b>Популярные запросы:</b>\n"
    for request_type, count in stats['popular_requests']:
        response += f"• {request_type}: {count}\n"
    response += "\n👤 <b>Последние пользователи:</b>\n"
    for user in stats['recent_users']:
        response += f"• {user[2]} {user[3]} (@{user[1]})\n"
    await query.message.reply_text(response, parse_mode='HTML')

async def start_callback(query):
    welcome_text = (
        f"🎓 Добро пожаловать в {UNIVERSITY_INFO['name']}!\n\n"
        "Выберите нужный раздел:"
    )
    keyboard = get_main_keyboard()
    if is_admin(query.from_user.id):
        new_keyboard = [list(row) for row in keyboard.inline_keyboard]
        new_keyboard.append([InlineKeyboardButton("👨‍💻 Админ-панель", callback_data="admin")])
        keyboard = InlineKeyboardMarkup(new_keyboard)
    await query.edit_message_text(welcome_text, reply_markup=keyboard)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text.lower()
    db.add_request(user.id, "message", text)

    if any(word in text for word in ['привет', 'здравств', 'start', 'hello']):
        await start(update, context)
    elif any(word in text for word in ['контакт', 'телефон', 'email', 'почта']):
        await update.message.reply_text(get_contacts_text(), parse_mode='HTML')
    elif any(word in text for word in ['адрес', 'корпус', 'метро', 'карта']):
        await update.message.reply_text(get_campuses_text(), parse_mode='HTML')
    elif any(word in text for word in ['поступлен', 'абитур', 'документ']):
        await update.message.reply_text(get_admission_text(), parse_mode='HTML')
    elif any(word in text for word in ['факультет', 'специальность', 'обучен']):
        await update.message.reply_text(get_faculties_text(), parse_mode='HTML')
    elif any(word in text for word in ['филиал', 'город']):
        await update.message.reply_text(get_branches_text(), parse_mode='HTML')
    elif any(word in text for word in ['помощь', 'help']):
        await update.message.reply_text(get_help_text(), parse_mode='HTML')
    elif any(word in text for word in ['статистика', 'stats']) and is_admin(user.id):
        stats = db.get_user_stats()
        if stats:
            response = "📊 <b>Статистика бота</b>\n\n"
            response += f"👥 Всего пользователей: <b>{stats['total_users']}</b>\n"
            response += f"📨 Всего запросов: <b>{stats['total_requests']}</b>\n"
            await update.message.reply_text(response, parse_mode='HTML')
        else:
            await update.message.reply_text("❌ Не удалось получить статистику.")
    else:
        await update.message.reply_text(
            "Извините, я не понял ваш запрос. Попробуйте использовать кнопки меню или задайте вопрос иначе."
        )

def get_contacts_text():
    contacts = UNIVERSITY_INFO['contacts']
    return (
        f"📞 <b>Контактная информация</b>\n\n"
        f"<b>Телефон:</b> {contacts['phone']}\n"
        f"<b>Доп. телефон:</b> {contacts['secondary_phone']}\n"
        f"<b>Email:</b> {contacts['email']}\n\n"
        f"<b>Сайты:</b>\n"
        f"• {contacts['website']}\n"
        f"• {contacts['admission_site']}\n\n"
        f"<b>Часы работы:</b>\n"
        f"Пн-Пт: {UNIVERSITY_INFO['working_hours']['weekdays']}\n"
        f"Сб-Вс: {UNIVERSITY_INFO['working_hours']['weekends']}"
    )

def get_campuses_text():
    text = "🏫 <b>Корпуса университета</b>\n\n"
    for campus in UNIVERSITY_INFO['campuses']:
        text += f"<b>{campus['name']}</b>\n"
        text += f"📍 Адрес: {campus['address']}\n"
        text += f"🚇 Метро: {campus['metro']}\n"
        text += f"🕒 Часы работы: {campus['hours']}\n\n"
    return text

def get_admission_text():
    admission = UNIVERSITY_INFO['admission']
    features = "\n".join([f"• {feature}" for feature in admission['features']])
    return (
        f"⏰ <b>Приёмная комиссия</b>\n\n"
        f"<b>Необходимые документы:</b>\n"
        f"{admission['documents']}\n\n"
        f"<b>Особенности:</b>\n"
        f"{features}\n\n"
        f"<b>Контакты:</b>\n"
        f"Телефон: {UNIVERSITY_INFO['contacts']['phone']}"
    )

def get_faculties_text():
    faculties = "\n".join([f"• {faculty}" for faculty in UNIVERSITY_INFO['faculties']])
    return (
        f"📝 <b>Факультеты и специальности</b>\n\n"
        f"{faculties}\n\n"
        f"<b>Для подробной информации:</b>\n"
        f"Обратитесь в приёмную комиссию: {UNIVERSITY_INFO['contacts']['phone']}"
    )

def get_branches_text():
    return (
        f"🌐 <b>Филиалы университета</b>\n\n"
        f"Университет имеет филиалы в большинстве крупных городов России.\n\n"
        f"<b>Для информации о конкретном филиале:</b>\n"
        f"Обратитесь в центральный офис: {UNIVERSITY_INFO['contacts']['phone']}\n"
        f"Или посетите сайт: {UNIVERSITY_INFO['contacts']['website']}"
    )

def get_help_text():
    return (
        f"🆘 <b>Помощь</b>\n\n"
        f"<b>Доступные команды:</b>\n"
        f"/start - начать диалог с ботом\n"
        f"/help - показать эту справку\n\n"
        f"<b>Вы также можете спросить:</b>\n"
        f"• О контактах университета\n"
        f"• Об адресах корпусов\n"
        f"• О поступлении и документах\n"
        f"• О факультетах и специальностях\n"
        f"• О филиалах университета\n\n"
        f"<b>Техническая поддержка:</b>\n"
        f"Если у вас возникли проблемы, обратитесь по email: {UNIVERSITY_INFO['contacts']['email']}"
    )