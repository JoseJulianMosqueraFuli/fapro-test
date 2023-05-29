from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException
from app.scraper import get_uf_value
from app.models import UFRequest


app = FastAPI()


@app.post("/uf")
def uf(data: UFRequest):
    """
    Endpoint para obtener el valor de UF para una fecha específica.
    """
    date_str = data.date

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        current_date = datetime.utcnow().date()
        max_date = current_date + timedelta(days=11)

        if date.year < 2013 or date.year > current_date.year:
            raise ValueError(
                "Año inválido. Asegúrate de que el año esté dentro del rango disponible."
            )

        # Validar la fecha maxima para no imprimir resultados vacios " "
        if date > max_date:
            raise ValueError(
                "Fecha inválida. Asegúrate de que la fecha esté dentro del rango disponible."
            )

    except ValueError as e:
        error_detail = str(e)  # Obtener el mensaje de error original
        if "day is out of range for month" in error_detail:
            error_detail = (
                "Día inválido. El mes especificado no tiene suficientes días."
            )
        elif "unconverted data remains" in error_detail or "time data" in error_detail:
            error_detail = "Fecha inválida. El formato correcto es 'YYYY-MM-DD' revisa puedes haber escrito un día o un més que no es valido."
        else:
            error_detail = "Error en la fecha especificada: " + error_detail

        raise HTTPException(status_code=400, detail=error_detail)

    try:
        uf_value = get_uf_value(date.day, date.month, date.year)
        return {"uf_value": uf_value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
