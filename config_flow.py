import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries

DOMAIN = "oskemenbus"

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required("stop_id"): cv.string,  # Обязательное поле для ввода ID остановки
    vol.Optional("buses", default=""): cv.string,  # Опциональное поле для ввода номеров автобусов через запятую
})


class OskemenBusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Конфигурационный поток для интеграции Oskemen Bus."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Обработка шага настройки пользователем."""
        if user_input is not None:
            # Здесь можно добавить валидацию данных или преобразование списка автобусов
            return self.async_create_entry(title="Oskemen Bus", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors={},
        )
