import requests
import json
import pytest
import swapi


class TestSwapi:

    def test_start_page(self, setup_function, teardown_function):
        """
        Проверка стартовой страницы
        """
        session = requests.session()
        url = "https://swapi.co/api/"
        resp = session.get(url)
        assert resp.status_code == 200


    def test_allowed_methods(self, setup_function, teardown_function):
        """
        Проверка разрешённых методов для запроса и получения данных
        """
        resp_get = requests.get("https://swapi.co/api/planets/1")
        assert resp_get.status_code == 200

        # Приводит к перенаправлению (не соответствует документации)
        resp_head = requests.head("https://swapi.co/api/planets/1")
        assert resp_head.status_code == 200

        resp_options = requests.options("https://swapi.co/api/planets/1", headers={'Content-type': 'application/json'})
        assert resp_options.status_code == 200


    def test_not_allowed_methods(self, setup_function, teardown_function):
        """
        Проверка запрещённых методов для запроса и получения данных
        """
        # Работает (не соответствует документации - метода POST нет среди разрешённых)
        resp = requests.post("https://swapi.co/api/planets/1", headers={'Content-type': 'application/json'},
                             json={"name": "Betelgeuse", "diameter": "100000001"})
        assert resp.status_code == 405

        resp = requests.put("https://swapi.co/api/planets/1", json={"name": "Betelgeuse", "diameter": "100000001"})
        assert resp.status_code == 405

        resp = requests.delete("https://swapi.co/api/planets/1")
        assert resp.status_code == 405


    def test_json(self, setup_function, teardown_function):
        """
        Проверка формата получаемых данных (json)
        """
        resp = requests.get("https://swapi.co/api/planets/1")
        assert resp.status_code == 200
        assert 'application/json' in resp.headers['Content-Type']


    def test_number_of_planets(self, setup_function, teardown_function):
        """
        Проверка общего количества планет, соответствие документации
        """
        resp = requests.get("https://swapi.co/api/planets")
        assert resp.status_code == 200
        json_decoded_result = resp.json()
        number_of_planets = json_decoded_result['count']
        assert number_of_planets == 61


    def test_all_planets_attributes(self, setup_function, teardown_function):
        """
        Проверка атрибутов всех планет внутри полученного json
        """
        resp = requests.get("https://swapi.co/api/planets")
        assert resp.status_code == 200
        json_decoded_result = resp.json()
        # Получение количества планет
        number_of_planets = json_decoded_result['count']

        # Атрибуты планет
        planets_attributes = ["name", "rotation_period", "orbital_period", "diameter", "climate",
                              "gravity", "terrain", "surface_water", "population", "residents",
                              "films", "created", "edited", "url"]

        # Проверка атрибутов в json для каждой из планет
        for planet in range(1, number_of_planets + 1):
            resp = requests.get("https://swapi.co/api/planets/{}".format(planet))
            assert resp.status_code == 200
            json_decoded_result = resp.json()

            for key, value in json_decoded_result.items():
                assert key in planets_attributes
                assert isinstance(value, (str, list))
