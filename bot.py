import requests
import yfinance as yf

TOKEN = "8481722365:AAF8E3Y71kHkIfSfcIZUoAD1i-AjgDff9wc"
CHAT_ID = "8725494993"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=payload)

def obtener_precio(simbolo):
    accion = yf.Ticker(simbolo)
    precio = accion.fast_info.last_price
    return precio

def enviar_portafolio(acciones):
    lineas = ["Portafolio de acciones:\n"]
    for simbolo in acciones:
        try:
            precio = obtener_precio(simbolo)
            lineas.append(f"{simbolo:<10} ${precio:.2f}")
        except Exception:
            lineas.append(f"{simbolo:<10} Error")
    send_message("\n".join(lineas))

if __name__ == "__main__":
    mis_acciones = ["AAPL", "TSLA", "MSFT", "GOOGL"]
    enviar_portafolio(mis_acciones)
