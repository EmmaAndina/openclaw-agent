import os
import logging
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# AI Configuration
ai_api_key = os.environ.get("AI_API_KEY")
ai_base_url = os.environ.get("AI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
ai_model = os.environ.get("AI_MODEL", "gemini-2.5-flash")

if ai_api_key:
    client = AsyncOpenAI(api_key=ai_api_key, base_url=ai_base_url)
    logging.info("AI Client initialized successfully.")
else:
    client = None
    logging.warning("AI_API_KEY environment variable is not set. The bot will fallback to basic echo mode.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu agente OpenClaw impulsado por IA. ¿En qué te ayudo?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not client:
        await update.message.reply_text(f"[Modo Eco / Faltan credenciales IA]: {user_text}")
        return

    try:
        response = await client.chat.completions.create(
            model=ai_model,
            messages=[
                {"role": "system", "content": "Eres un asistente de Inteligencia Artificial llamado OpenClaw, un rol similar a un ingeniero de software experto de Z.AI interactuando vía Telegram con el usuario. Tus respuestas deben ser cortas, útiles y resolver sus problemas técnicos."},
                {"role": "user", "content": user_text}
            ],
            max_tokens=1000
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        logging.error(f"Error calling AI: {e}")
        await update.message.reply_text("Lo siento, ocurrió un error al procesar tu solicitud con la IA.")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong! 🏓 El agente de IA está activo.")

# Dummy HTTP server for health checks required by Coolify deployment
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, format, *args):
        pass

def run_health_server():
    port = int(os.environ.get("PORT", 80))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()

if __name__ == '__main__':
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    if not telegram_token:
        logging.error("TELEGRAM_TOKEN is not set.")
        exit(1)

    # Start health server in background
    threading.Thread(target=run_health_server, daemon=True).start()

    application = ApplicationBuilder().token(telegram_token).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('ping', ping))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    logging.info("Starting OpenClaw Telegram Bot with AI Integration...")
    application.run_polling()
