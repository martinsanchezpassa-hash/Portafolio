import os
import time
import requests
import schedule
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

MIS_ACCIONES = ["AAPL", "TSLA", "MSFT", "GOOGL"]


def obtener_precio(simbolo):
    yf.set_tz_cache_location(None)
    accion = yf.Ticker(simbolo)
    # download fuerza petición HTTP fresca, sin caché local
    df = yf.download(simbolo, period="1d", interval="1m", progress=False)
    if df.empty:
        raise ValueError(f"Sin datos para {simbolo}")
    return float(df["Close"].iloc[-1])


def construir_resumen(acciones):
    lineas = ["📊 *Resumen del Portafolio*\n"]
    lineas.append(f"{'Símbolo':<8} {'Precio (USD)':>12}")
    lineas.append("─" * 22)
    for simbolo in acciones:
        try:
            precio = obtener_precio(simbolo)
            lineas.append(f"{simbolo:<8} ${precio:>11.2f}")
        except Exception:
            lineas.append(f"{simbolo:<8} {'Error':>12}")
    return "\n".join(lineas)


def enviar_mensaje(texto):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown",
    }
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()


def enviar_resumen():
    print("Enviando resumen del portafolio...")
    resumen = construir_resumen(MIS_ACCIONES)
    enviar_mensaje(f"```\n{resumen}\n```")
    print("Resumen enviado.")


def validar_config():
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN no está configurado en .env")
    if not CHAT_ID:
        raise ValueError("CHAT_ID no está configurado en .env")


if __name__ == "__main__":
    validar_config()
    # Envía un resumen inmediatamente al iniciar (opcional, comenta si no lo deseas)
    enviar_resumen()

    # Programa el envío diario a las 09:00
    schedule.every().day.at("09:00").do(enviar_resumen)
    print("Bot activo. Enviará el resumen diariamente a las 09:00.")

    while True:
        schedule.run_pending()
        time.sleep(30)
