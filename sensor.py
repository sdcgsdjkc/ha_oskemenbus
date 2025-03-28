import logging
from homeassistant.helpers.entity import Entity
from .bus_parser import fetch_bus_data  # Импорт функции парсера

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Настройка сенсоров через config flow."""
    data = config_entry.data
    stop_id = data.get("stop_id")
    buses = data.get("buses")
    async_add_entities([OskemenBusSensor(stop_id, buses)], update_before_add=True)

class OskemenBusSensor(Entity):
    """Сенсор для отображения расписания автобусов."""

    def __init__(self, stop_id, buses):
        self._stop_id = stop_id
        self._buses = buses
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return f"Oskemen Bus {self._stop_id}"

    @property
    def state(self):
        """Состояние сенсора – количество найденных маршрутов."""
        return self._state

    @property
    def extra_state_attributes(self):
        """
        Дополнительные атрибуты сенсора с подробной информацией:
        - stop_id
        - routes: список маршрутов, каждый со своим номером, конечной остановкой и временем прибытия.
        """
        return self._attributes

    async def async_update(self):
        """Обновление данных сенсора с помощью парсера."""
        data = await fetch_bus_data(self._stop_id, self._buses)
        if not data:
            self._state = "Ошибка получения данных"
            self._attributes = {}
            return

        routes = data.get("routes", [])
        self._state = f"Найдено маршрутов: {len(routes)}"

        # Формируем список подробных данных по маршрутам
        routes_info = []
        for route in routes:
            number = route.get("number")
            end_stop = route.get("end_stop")
            arrival_times = route.get("arrival_times", [])
            # Формируем строку вида: "Маршрут 1 (Защита): через 4 минуты, через 22 минуты"
            route_str = f"Маршрут {number} ({end_stop}): " + ", ".join(arrival_times)
            routes_info.append(route_str)

        self._attributes = {
            "stop_id": self._stop_id,
            "routes": routes_info
        }
