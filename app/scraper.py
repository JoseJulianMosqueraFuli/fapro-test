from bs4 import BeautifulSoup
import requests


def get_uf_value(day, month, year):
    """
    Obtiene el valor de UF para una fecha específica.
    """
    url = f"https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm"
    response = requests.get(url)
    response.raise_for_status()

    bs = BeautifulSoup(response.text, "lxml")
    table = bs.find("div", attrs={"id": "mes_all"}).find("tbody")
    rows = table.find_all("tr")

    required_column = month - 1
    column_values = [row.find_all("td")[required_column].text for row in rows]

    return column_values[day - 1]