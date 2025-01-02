import os
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram import Update

# Command handler function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command"""
    await update.message.reply_text('Hello! I am your bot!')

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /hello command"""
    await update.message.reply_text('Hello! this is hello function!')


BOT_TOKEN = os.environ.get('BOT_TOKEN')
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    hello_handler = CommandHandler('hello', hello)
    application.add_handler(start_handler)
    application.add_handler(hello_handler)
    
    application.run_polling()

if __name__ == "__main__":
   main()