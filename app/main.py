from datetime import datetime

from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
import requests

app = FastAPI()


def get_uf_value(day, month, year):
    url = f"https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm"
    response = requests.get(url)
    response.raise_for_status()

    bs = BeautifulSoup(response.text, "lxml")
    table = bs.find("div", attrs={"id": "mes_all"}).find("tbody")
    rows = table.find_all("tr")

    required_column = month - 1
    column_values = [row.find_all("td")[required_column].text for row in rows]

    return column_values[day - 1]


@app.post("/uf")
def uf(data: dict):
    date_str = data.get("date")

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Fecha inválida. El formato correcto es 'YYYY-MM-DD' de las opciones posibles",
        )

    if date.year < 2013 or date.year > datetime.now().year:
        raise HTTPException(
            status_code=400,
            detail="Año inválido. Asegúrate de que el año esté dentro del rango disponible.",
        )

    try:
        uf_value = get_uf_value(date.day, date.month, date.year)
        return {"uf_value": uf_value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
