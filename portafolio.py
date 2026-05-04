import yfinance as yf

def obtener_precio(simbolo):
    accion = yf.Ticker(simbolo)
    info = accion.fast_info
    precio = info.last_price
    return precio

def mostrar_portafolio(acciones):
    print(f"\n{'Símbolo':<10} {'Precio (USD)':>15}")
    print("-" * 27)
    for simbolo in acciones:
        try:
            precio = obtener_precio(simbolo)
            print(f"{simbolo:<10} {precio:>15.2f}")
        except Exception:
            print(f"{simbolo:<10} {'Error':>15}")

if __name__ == "__main__":
    # Agrega aquí tus acciones
    mis_acciones = ["AAPL", "TSLA", "MSFT", "GOOGL"]
    mostrar_portafolio(mis_acciones)
