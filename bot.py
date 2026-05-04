import time
import schedule
import requests
import yfinance as yf
from datetime import datetime

TOKEN = "8481722365:AAF8E3Y71kHkIfSfcIZUoAD1i-AjgDff9wc"
CHAT_ID = 8725494993

# Portafolio: (unidades, precio_promedio, moneda_base)
PORTFOLIO = {
    "CHILE.SN": (1200,    168.4,    "CLP"),
    "LTM.SN":   (16379,   22.07,    "CLP"),
    "SQM-B.SN": (4,       79740.5,  "CLP"),
    "SOXL":     (0.877,   125.25,   "USD"),
    "SPY":      (0.316,   713.87,   "USD"),
    "SSO":      (2.431,   81.51,    "USD"),
    "XES":      (2.236,   127.87,   "USD"),
}

def get_usd_clp():
    try:
        ticker = yf.Ticker("USDCLP=X")
        return ticker.fast_info.last_price
    except Exception:
        return None

def get_price(symbol):
    ticker = yf.Ticker(symbol)
    return ticker.fast_info.last_price

def build_message():
    usd_clp = get_usd_clp()
    now = datetime.now().strftime("%d/%m/%Y %H:%M")

    clp_cost   = 0.0
    clp_value  = 0.0
    usd_cost   = 0.0
    usd_value  = 0.0

    lines = [f"📊 *Portafolio — {now}*\n"]

    for symbol, (units, avg_price, currency) in PORTFOLIO.items():
        try:
            price = get_price(symbol)
            cost        = units * avg_price
            value       = units * price
            pnl         = value - cost
            pnl_pct     = (pnl / cost * 100) if cost else 0
            arrow       = "🟢" if pnl >= 0 else "🔴"
            sign        = "+" if pnl >= 0 else ""
            cur_sym     = "CLP" if currency == "CLP" else "USD"

            lines.append(
                f"{arrow} *{symbol}*\n"
                f"   {units} u × {cur_sym} {price:,.2f}\n"
                f"   Valor: {cur_sym} {value:,.0f}  |  P&L: {sign}{cur_sym} {pnl:,.0f} ({sign}{pnl_pct:.1f}%)"
            )

            if currency == "CLP":
                clp_cost  += cost
                clp_value += value
            else:
                usd_cost  += cost
                usd_value += value

        except Exception as e:
            lines.append(f"⚠️ *{symbol}*: error al obtener precio")

    # Totales
    lines.append("\n─────────────────")

    clp_pnl     = clp_value - clp_cost
    clp_pnl_pct = (clp_pnl / clp_cost * 100) if clp_cost else 0
    usd_pnl     = usd_value - usd_cost
    usd_pnl_pct = (usd_pnl / usd_cost * 100) if usd_cost else 0

    sign_clp = "+" if clp_pnl >= 0 else ""
    sign_usd = "+" if usd_pnl >= 0 else ""

    lines.append(
        f"🇨🇱 *CLP total*\n"
        f"   Costo: CLP {clp_cost:,.0f}\n"
        f"   Valor: CLP {clp_value:,.0f}  |  P&L: {sign_clp}CLP {clp_pnl:,.0f} ({sign_clp}{clp_pnl_pct:.1f}%)"
    )
    lines.append(
        f"🇺🇸 *USD total*\n"
        f"   Costo: USD {usd_cost:,.2f}\n"
        f"   Valor: USD {usd_value:,.2f}  |  P&L: {sign_usd}USD {usd_pnl:,.2f} ({sign_usd}{usd_pnl_pct:.1f}%)"
    )

    if usd_clp:
        total_clp = clp_value + usd_value * usd_clp
        total_cost_clp = clp_cost + usd_cost * usd_clp
        total_pnl_clp = total_clp - total_cost_clp
        sign_t = "+" if total_pnl_clp >= 0 else ""
        lines.append(
            f"\n💼 *Total consolidado (USD/CLP {usd_clp:,.0f})*\n"
            f"   CLP {total_clp:,.0f}  |  P&L: {sign_t}CLP {total_pnl_clp:,.0f}"
        )

    return "\n".join(lines)

def send_report():
    text = build_message()
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Reporte enviado.")

if __name__ == "__main__":
    print("Enviando reporte inicial...")
    send_report()

    schedule.every().day.at("09:00").do(send_report)
    print("Programado para las 9:00 AM cada día. Esperando...")

    while True:
        schedule.run_pending()
        time.sleep(30)
