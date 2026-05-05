import sys
import yfinance as yf
from datetime import datetime

# ticker, nombre, cantidad, precio_promedio, moneda
ACCIONES = [
    ("CHILE.SN", "Banco de Chile",         1.200,  168.40,   "CLP"),
    ("LTM",      "LATAM Airlines",        16.379,   22.07,   "CLP"),
    ("SQM-B.SN", "SQM-B",                  4.000, 79740.50,  "CLP"),
    ("SOXL",     "Semiconductores 3x",     0.877,  125.25,   "USD"),
    ("SPY",      "ETF S&P 500",            0.316,  713.67,   "USD"),
    ("SSO",      "ProShares Ultra S&P 2x", 2.431,   81.51,   "USD"),
    ("XES",      "Oil & Gas Services",     2.236,  127.87,   "USD"),
]

# Tickers con más cobertura de noticias en inglés
TICKER_NOTICIAS = {
    "CHILE.SN": "BCH",
    "SQM-B.SN": "SQM",
}


def obtener_precio(ticker):
    return yf.Ticker(ticker).fast_info.last_price


def mostrar_portafolio():
    print(f"\n{'Acción':<24} {'Cant':>6} {'P.Prom':>10} {'Precio':>10} {'Retorno':>12} {'%':>7}  Mon")
    print("-" * 78)
    for ticker, nombre, cantidad, precio_prom, moneda in ACCIONES:
        try:
            precio = obtener_precio(ticker)
            retorno = (precio - precio_prom) * cantidad
            pct = ((precio / precio_prom) - 1) * 100
            flecha = "↑" if retorno >= 0 else "↓"
            print(f"{nombre:<24} {cantidad:>6.3f} {precio_prom:>10.2f} {precio:>10.2f} {flecha}{abs(retorno):>11.2f} {pct:>+6.2f}%  {moneda}")
        except Exception:
            print(f"{nombre:<24} {'— error al obtener precio —':>50}")


def _extraer_titulo(noticia):
    # yfinance puede devolver distintas estructuras según la versión
    content = noticia.get("content", {})
    return (
        content.get("title")
        or noticia.get("title")
        or "Sin título"
    )


def _extraer_fecha(noticia):
    content = noticia.get("content", {})
    return content.get("pubDate") or noticia.get("providerPublishTime", "")


def contexto():
    print(f"\n{'='*62}")
    print(f"  NOTICIAS DEL PORTAFOLIO — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"{'='*62}")

    for ticker, nombre, *_ in ACCIONES:
        ticker_news = TICKER_NOTICIAS.get(ticker, ticker)
        try:
            noticias = yf.Ticker(ticker_news).news or []
            print(f"\n  {nombre} ({ticker})")
            print(f"  {'-'*50}")
            if not noticias:
                print("  Sin noticias recientes.")
                continue
            for n in noticias[:3]:
                titulo = _extraer_titulo(n)
                fecha = _extraer_fecha(n)
                fecha_str = f"  [{fecha}]" if fecha else ""
                print(f"  • {titulo}{fecha_str}")
        except Exception:
            print(f"  Sin noticias disponibles.")

    print()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "contexto":
        contexto()
    else:
        mostrar_portafolio()
