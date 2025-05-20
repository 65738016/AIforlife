import os
import logging
import openai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

openai_api_key = os.getenv("OPENAI_API_KEY")
bot_token = os.getenv("BOT_TOKEN")

if not openai_api_key or not bot_token:
    raise RuntimeError("Debes definir las variables de entorno OPENAI_API_KEY y BOT_TOKEN.")

openai.api_key = openai_api_key

user_db = {}

def register_user(user_id: int):
    if user_id not in user_db:
        user_db[user_id] = {"vip": False}
        logging.info(f"Usuario nuevo registrado: {user_id}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    register_user(user_id)
    await update.message.reply_text(
        "¡Hola! Soy AIforlife33 🤖✨\nEstoy aquí para responder tus preguntas y generar imágenes con inteligencia artificial.\n\nEscribe tu mensaje o usa el comando /imagen seguido de una idea."
    )

async def imagen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not context.args:
            await update.message.reply_text("Escribe un prompt para generar una imagen.")
            return
        prompt = " ".join(context.args)
        response = openai.images.generate(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        image_url = getattr(response.data[0], "url", None)
        if image_url:
            await update.message.reply_photo(photo=image_url)
        else:
            await update.message.reply_text("No se pudo generar la imagen. Intenta con otro prompt.")
    except Exception as e:
        logging.error(f"Error con OpenAI (Imagen): {e}")
        await update.message.reply_text(f"Ocurrió un error al generar la imagen: {str(e)}")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        prompt = update.message.text
        if not prompt:
            await update.message.reply_text("Por favor escribe un mensaje para chatear.")
            return
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = getattr(response.choices[0].message, "content", None)
        if reply:
            await update.message.reply_text(reply)
        else:
            await update.message.reply_text("No se recibió respuesta de la IA. Intenta de nuevo.")
    except Exception as e:
        logging.error(f"Error con OpenAI (Chat): {e}")
        await update.message.reply_text(f"Ocurrió un error al procesar tu solicitud: {str(e)}")

def main():
    application = ApplicationBuilder().token(bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("imagen", imagen))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    logging.info("Bot iniciado correctamente.")
    application.run_polling()

if __name__ == "__main__":
    main()
