from bs4 import BeautifulSoup
from fastapi import HTTPException
import requests
import requests_cache

requests_cache.install_cache("uf_cache")


def get_uf_value(day, month, year):
    """
    Obtiene el valor de UF para una fecha específica.
    """
    try:
        url = f"https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm"
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        bs = BeautifulSoup(response.text, "html.parser")
        table = bs.find("div", attrs={"id": "mes_all"}).find("tbody")
        rows = table.find_all("tr")

        required_column = month - 1
        column_values = [row.find_all("td")[required_column].text for row in rows]

        uf_value = column_values[day - 1]

        if uf_value.strip() == "":
            raise HTTPException(
                status_code=404,
                detail="Valor de UF no disponible para la fecha especificada.",
            )

        return uf_value

    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=500, detail=str(e))
