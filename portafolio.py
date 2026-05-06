import yfinance as yf

# Posiciones: símbolo -> (cantidad_acciones, precio_promedio)
MIS_POSICIONES = {
    "AAPL":  (10,   150.00),
    "TSLA":  (5,    200.00),
    "MSFT":  (8,    300.00),
    "GOOGL": (3,    140.00),
    "SOXL":  (2.66, 145.54),  # Direxion Daily Semiconductor Bull 3x Shares
}

def obtener_datos(simbolo):
    accion = yf.Ticker(simbolo)
    info = accion.fast_info
    precio_actual = info.last_price
    precio_cierre_anterior = info.previous_close
    return precio_actual, precio_cierre_anterior

def mostrar_portafolio(posiciones):
    print(f"\n{'Símbolo':<8} {'Nombre':<45} {'Precio':>10} {'Cambio%':>8} {'Acciones':>9} {'P.Prom':>10} {'Retorno$':>10} {'Retorno%':>9}")
    print("-" * 115)

    total_invertido = 0
    total_valor = 0

    for simbolo, (cantidad, precio_promedio) in posiciones.items():
        try:
            precio_actual, precio_anterior = obtener_datos(simbolo)
            cambio_dia_pct = ((precio_actual - precio_anterior) / precio_anterior) * 100 if precio_anterior else 0

            valor_actual = precio_actual * cantidad
            costo = precio_promedio * cantidad
            retorno = valor_actual - costo
            retorno_pct = (retorno / costo) * 100 if costo else 0

            ticker = yf.Ticker(simbolo)
            nombre = ticker.info.get("shortName", simbolo)[:43]

            signo_dia = "+" if cambio_dia_pct >= 0 else ""
            signo_ret = "+" if retorno >= 0 else ""

            print(
                f"{simbolo:<8} {nombre:<45} {precio_actual:>10.2f} "
                f"{signo_dia}{cambio_dia_pct:>7.2f}% {cantidad:>9.2f} "
                f"{precio_promedio:>10.2f} {signo_ret}{retorno:>9.2f} "
                f"{signo_ret}{retorno_pct:>8.2f}%"
            )

            total_invertido += costo
            total_valor += valor_actual

        except Exception as e:
            print(f"{simbolo:<8} {'Error al obtener datos':<45} {str(e)}")

    retorno_total = total_valor - total_invertido
    retorno_total_pct = (retorno_total / total_invertido) * 100 if total_invertido else 0
    signo = "+" if retorno_total >= 0 else ""

    print("-" * 115)
    print(f"{'TOTAL':<54} Invertido: ${total_invertido:>10.2f}   Valor: ${total_valor:>10.2f}   Retorno: {signo}${retorno_total:.2f} ({signo}{retorno_total_pct:.2f}%)")

if __name__ == "__main__":
    mostrar_portafolio(MIS_POSICIONES)
