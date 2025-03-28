import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

async def fetch_bus_data(stop_id: str, buses: str):
    url = "http://192.168.1.114:8000/api/bus/schedule"
    payload = {"stop_id": stop_id}
    _LOGGER.info("Отправка POST-запроса к %s с payload: %s", url, payload)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                _LOGGER.info("Получен ответ с кодом %s", response.status)
                if response.status != 200:
                    _LOGGER.error("Ошибка запроса: статус %s", response.status)
                    return None
                data = await response.json()
                _LOGGER.debug("Данные, полученные от FastAPI: %s", data)
                if buses:
                    filter_routes = [b.strip() for b in buses.split(",") if b.strip()]
                    data["routes"] = [
                        route for route in data.get("routes", [])
                        if route.get("number") in filter_routes
                    ]
                    _LOGGER.info("Данные после фильтрации: %s", data)
                return data
    except Exception as e:
        _LOGGER.error("Ошибка получения данных для остановки %s: %s", stop_id, e)
        return None
