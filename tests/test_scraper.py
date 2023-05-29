from fastapi import HTTPException
import requests
from unittest import mock
import pytest

from app.scraper import get_uf_value


class TestScraper:
    @pytest.fixture
    def mock_response(self, mocker):
        response_mock = mocker.Mock()
        response_mock.raise_for_status.return_value = None
        response_mock.text = (
            "<div id='mes_all'><tbody><tr><td>1000.00</td></tr></tbody></div>"
        )
        return response_mock

    @pytest.fixture
    def mock_requests_get(self, mocker, mock_response):
        get_mock = mocker.patch("requests.get")
        get_mock.return_value = mock_response
        return get_mock

    def test_get_uf_value_valid_date(self, mocker, mock_requests_get):
        day = 1
        month = 1
        year = 2022
        expected_uf_value = "1000.00"

        uf_value = get_uf_value(day, month, year)

        assert uf_value == expected_uf_value
        mock_requests_get.assert_called_once_with(
            f"https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm", timeout=5
        )

    def test_get_uf_value_invalid_date(self):
        day = 0
        month = 0
        year = 0

        with pytest.raises(HTTPException):
            get_uf_value(day, month, year)

    # Test para intentar replicar el comportamiento de un valor vacio ""
    # def test_get_uf_value_unavailable_uf(self, mocker, mock_requests_get):
    #     mock_response = mocker.Mock()
    #     mock_response.text = (
    #         "<div id='mes_all'><tbody><tr><td> </td></tr></tbody></div>"
    #     )
    #     mock_requests_get.return_value = mock_response

    #     day = 31
    #     month = 4
    #     year = 2022

    #     with pytest.raises(HTTPException):
    #         get_uf_value(day, month, year)

    def test_get_uf_value_http_error(self, mocker, mock_requests_get):
        mock_requests_get.side_effect = requests.exceptions.HTTPError()

        day = 1
        month = 1
        year = 2022

        with pytest.raises(HTTPException):
            get_uf_value(day, month, year)
