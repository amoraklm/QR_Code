import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from flask import Flask

# Flask app برای health check
web_app = Flask(__name__)

@web_app.route('/health')
def health_check():
    return "OK", 200

@web_app.route('/')
def home():
    return "🤖 Telegram Bot is Running on Fly.io!", 200

class TelegramBot:
    def __init__(self):
        self.token = os.environ.get('BOT_TOKEN')
        if not self.token:
            raise ValueError("BOT_TOKEN not set")
        
        self.application = Application.builder().token(self.token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo))
    
    async def start(self, update: Update, context: CallbackContext):
        await update.message.reply_text('🚀 ربات روی Fly.io فعال است!')
    
    async def echo(self, update: Update, context: CallbackContext):
        await update.message.reply_text(f'پیام شما: {update.message.text}')
    
    def run(self):
        # استفاده از polling برای سادگی
        self.application.run_polling()

if __name__ == '__main__':
    # اجرای Flask در thread جداگانه
    import threading
    flask_thread = threading.Thread(
        target=lambda: web_app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False),
        daemon=True
    )
    flask_thread.start()
    
    # اجرای ربات تلگرام
    bot = TelegramBot()
    bot.run()
