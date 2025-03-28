import logging
from homeassistant.helpers.entity import Entity
from .bus_parser import fetch_bus_data

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    data = config_entry.data
    stop_id = data.get("stop_id")
    buses = data.get("buses")
    _LOGGER.info("Настройка сенсоров для остановки: %s, автобусы: %s", stop_id, buses)
    async_add_entities([OskemenBusSensor(stop_id, buses)], update_before_add=True)

class OskemenBusSensor(Entity):
    def __init__(self, stop_id, buses):
        self._stop_id = stop_id
        self._buses = buses
        self._state = None
        self._attributes = {}
        _LOGGER.info("Создан сенсор OskemenBusSensor для остановки: %s", stop_id)

    @property
    def name(self):
        return f"Oskemen Bus {self._stop_id}"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    async def async_update(self):
        _LOGGER.info("Обновление данных для сенсора остановки %s", self._stop_id)
        data = await fetch_bus_data(self._stop_id, self._buses)
        if not data:
            self._state = "Ошибка получения данных"
            self._attributes = {}
            _LOGGER.error("fetch_bus_data вернул None для остановки %s", self._stop_id)
            return

        routes = data.get("routes", [])
        self._state = f"Найдено маршрутов: {len(routes)}"
        _LOGGER.info("Для остановки %s найдено %d маршрутов", self._stop_id, len(routes))

        routes_info = []
        for route in routes:
            number = route.get("number")
            end_stop = route.get("end_stop")
            arrival_times = route.get("arrival_times", [])
            route_str = f"Маршрут {number} ({end_stop}): " + ", ".join(arrival_times)
            routes_info.append(route_str)

        self._attributes = {
            "stop_id": self._stop_id,
            "routes": routes_info
        }
        _LOGGER.debug("Атрибуты сенсора для остановки %s: %s", self._stop_id, self._attributes)
