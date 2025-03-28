import logging
from homeassistant.components.sensor import SensorEntity
from .oskemenbus_parser.main import fetch_bus_data

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    data = config_entry.data
    stop_id = data.get("stop_id")
    buses = data.get("buses")
    _LOGGER.info("Настройка сенсора для остановки: %s, автобусы: %s", stop_id, buses)
    async_add_entities([OskemenBusSensor(stop_id, buses)], update_before_add=True)

class OskemenBusSensor(SensorEntity):
    def __init__(self, stop_id, buses):
        self._stop_id = stop_id
        self._buses = buses
        self._state = None
        self._attributes = {}
        _LOGGER.info("Создан сенсор для остановки: %s", stop_id)

    @property
    def name(self):
        return f"Oskemen Bus {self._stop_id}"

    @property
    def state(self):
        return self._state

    @property
    def attributes(self):
        return self._attributes

    async def async_update(self):
        _LOGGER.info("Обновление данных для остановки %s", self._stop_id)
        data = await fetch_bus_data(self._stop_id, self._buses)
        if not data:
            self._state = "Ошибка"
            self._attributes = {}
            _LOGGER.error("fetch_bus_data вернул None для остановки %s", self._stop_id)
            return

        routes = data.get("routes", [])
        _LOGGER.info("Для остановки %s найдено %d маршрутов", self._stop_id, len(routes))

        routes_info = []
        for route in routes:
            number = route.get("number")
            end_stop = route.get("end_stop")
            arrival_times = route.get("arrival_times", [])
            if arrival_times:
                route_str = f"{number} ({end_stop}): {arrival_times[0]}"
            else:
                route_str = f"{number} ({end_stop}): Нет данных"
            routes_info.append(route_str)

        if routes_info:
            self._state = routes_info[0]  # Только первый маршрут
        else:
            self._state = "Нет данных"

        self._attributes = {
            "stop_id": self._stop_id,
            "routes": routes_info
        }
        _LOGGER.debug("Обновлены данные сенсора для остановки %s: %s", self._stop_id, self._attributes)
