import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from portafolio import obtener_precio

TOKEN = os.getenv("TELEGRAM_TOKEN", "8481722365:AAF8E3Y71kHkIfSfcIZUoAD1i-AjgDff9wc")

MIS_ACCIONES = ["AAPL", "TSLA", "MSFT", "GOOGL"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola! Comandos disponibles:\n"
        "/portafolio — ver precios de tus acciones\n"
        "/precio <SIMBOLO> — consultar una acción específica"
    )


async def portafolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lines = ["📊 *Tu Portafolio*\n"]
    for simbolo in MIS_ACCIONES:
        try:
            precio = obtener_precio(simbolo)
            lines.append(f"`{simbolo:<6}` — ${precio:,.2f}")
        except Exception:
            lines.append(f"`{simbolo:<6}` — Error al obtener precio")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /precio <SIMBOLO>  ej: /precio AAPL")
        return
    simbolo = context.args[0].upper()
    try:
        p = obtener_precio(simbolo)
        await update.message.reply_text(f"`{simbolo}` — ${p:,.2f}", parse_mode="Markdown")
    except Exception:
        await update.message.reply_text(f"No se pudo obtener el precio de `{simbolo}`.", parse_mode="Markdown")


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("portafolio", portafolio))
    app.add_handler(CommandHandler("precio", precio))
    print("Bot corriendo...")
    app.run_polling()
