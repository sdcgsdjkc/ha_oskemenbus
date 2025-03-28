import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

# Импортируем функцию из main.py (она должна быть написана так, чтобы её можно было импортировать)
from .oskemenbus_parser.main import get_schedule

_LOGGER = logging.getLogger(__name__)
_executor = ThreadPoolExecutor(max_workers=1)

async def fetch_bus_data(stop_id: str, buses: str):
    """
    Вызывает функцию get_schedule из main.py для получения расписания автобусов.
    Аргумент buses – строка с номерами маршрутов через запятую; если задан, происходит фильтрация результата.
    """
    try:
        # get_schedule, скорее всего, синхронная функция.
        # Запустим её в пуле потоков, чтобы не блокировать основной цикл HA.
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(_executor, get_schedule, stop_id)

        # Если указан фильтр по маршрутам, отфильтровываем их
        if buses:
            filter_routes = [b.strip() for b in buses.split(",") if b.strip()]
            data["routes"] = [
                route for route in data.get("routes", [])
                if route.get("number") in filter_routes
            ]
        return data

    except Exception as e:
        _LOGGER.error("Ошибка при получении данных для остановки %s: %s", stop_id, e)
        return None
