import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# تنظیمات logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class RailwayBot:
    def __init__(self):
        self.token = os.environ.get('BOT_TOKEN')
        if not self.token:
            raise ValueError("لطفا BOT_TOKEN را در محیط تنظیم کنید")
        
        self.application = Application.builder().token(self.token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo))
    
    async def start(self, update: Update, context: CallbackContext):
        user = update.effective_user
        await update.message.reply_text(
            f"👋 سلام {user.first_name}!\n"
            "🤖 ربات روی Railway فعال شد!\n\n"
            "🎵 امکانات:\n"
            "• دانلود موزیک\n"
            "• دانلود ویدیو\n"
            "• مدیریت گروه\n\n"
            "از /help کمک بگیرید."
        )
    
    async def help(self, update: Update, context: CallbackContext):
        help_text = """
📖 راهنمای ربات:

🔐 امنیت:
/security - مدیریت امنیت گروه

🎵 موزیک:
لینک یوتیوب ارسال کنید

🎬 ویدیو:
لینک یوتیوب ارسال کنید

ربات توسط Railway میزبانی میشود 🚄
        """
        await update.message.reply_text(help_text)
    
    async def echo(self, update: Update, context: CallbackContext):
        text = update.message.text
        if "youtube.com" in text or "youtu.be" in text:
            await update.message.reply_text("🎬 لینک یوتیوب دریافت شد! به زودی قابلیت دانلود اضافه میشه.")
        else:
            await update.message.reply_text(f"پیام شما: {text}")

    def run(self):
        # استفاده از webhook برای Railway
        PORT = int(os.environ.get('PORT', 8443))
        WEBHOOK_URL = os.environ.get('RAILWAY_STATIC_URL')
        
        if WEBHOOK_URL:
            # حالت Production - Webhook
            self.application.run_webhook(
                listen="0.0.0.0",
                port=PORT,
                url_path=self.token,
                webhook_url=f"{WEBHOOK_URL}/{self.token}"
            )
        else:
            # حالت Development - Polling
            self.application.run_polling()

if __name__ == '__main__':
    bot = RailwayBot()
    bot.run()
