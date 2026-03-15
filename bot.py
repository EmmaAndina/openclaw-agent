import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="¡Hola! Soy tu agente OpenClaw alojado en Hetzner (vía Coolify). ¿En qué puedo ayudarte?"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f"Recibí tu mensaje: {update.message.text}"
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Pong! 🏓 El agente está activo y funcionando correctamente."
    )

if __name__ == '__main__':
    # Use environment variable for the token
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    
    if not telegram_token:
        logging.error("TELEGRAM_TOKEN is not set in environment variables.")
        exit(1)

    # Initialize the telegram app
    application = ApplicationBuilder().token(telegram_token).build()
    
    # Add command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('ping', ping))
    
    # Add a catch-all message handler
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    
    # Start polling
    logging.info("Starting OpenClaw Telegram Bot...")
    application.run_polling()
