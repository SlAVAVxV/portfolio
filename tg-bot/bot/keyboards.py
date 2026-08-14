from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📞 Контакты", callback_data="contacts")],
        [InlineKeyboardButton("🏫 Корпуса", callback_data="campuses")],
        [InlineKeyboardButton("⏰ Приёмная комиссия", callback_data="admission")],
        [InlineKeyboardButton("🌐 Филиалы", callback_data="branches")],
        [InlineKeyboardButton("📝 Факультеты", callback_data="faculties")],
        [InlineKeyboardButton("🆘 Помощь", callback_data="help")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_keyboard():
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back")]]
    return InlineKeyboardMarkup(keyboard)

def get_admin_keyboard():
    keyboard = [
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ]
    return InlineKeyboardMarkup(keyboard)