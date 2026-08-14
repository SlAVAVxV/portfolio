import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot.config import BOT_TOKEN
from bot.handlers import start, button_handler, handle_message

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def error_handler(update, context):
    logger.error("Exception while handling an update:", exc_info=context.error)

def main():
    if BOT_TOKEN == "your_bot_token_here" or not BOT_TOKEN:
        print("ОШИБКА: Замените 'your_bot_token_here' на реальный токен вашего бота в файле .env!")
        return
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()