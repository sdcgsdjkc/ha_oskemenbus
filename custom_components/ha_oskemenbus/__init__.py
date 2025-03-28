import sys
import asyncio
import logging
from homeassistant import config_entries

DOMAIN = "ha_oskemenbus"
_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    _LOGGER.info("async_setup вызван для %s", DOMAIN)
    return True

async def async_setup_entry(hass, entry):
    _LOGGER.info("async_setup_entry вызван для %s с entry_id: %s", DOMAIN, entry.entry_id)
    # Формируем путь к main.py, который находится в подпапке oskemenbus_parser
    script_path = hass.config.path("custom_components", "ha_oskemenbus", "oskemenbus_parser", "main.py")
    _LOGGER.info("Запуск FastAPI-сервера из %s", script_path)
    try:
        process = await asyncio.create_subprocess_exec(
            sys.executable, script_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        hass.data.setdefault(DOMAIN, {})[entry.entry_id] = process
        _LOGGER.info("FastAPI-сервер успешно запущен")
    except Exception as e:
        _LOGGER.error("Ошибка запуска FastAPI-сервера: %s", e)
        return False

    try:
        await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
        _LOGGER.info("Платформа sensor успешно подключена")
    except Exception as e:
        _LOGGER.error("Ошибка при подключении платформы sensor: %s", e)

    return True

async def async_unload_entry(hass, entry):
    _LOGGER.info("async_unload_entry вызван для %s, entry_id: %s", DOMAIN, entry.entry_id)
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    if unload_ok:
        process = hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
        if process:
            process.terminate()
            try:
                await asyncio.wait_for(process.wait(), timeout=10)
                _LOGGER.info("FastAPI-сервер успешно остановлен")
            except asyncio.TimeoutError:
                _LOGGER.warning("Не удалось завершить FastAPI-сервер в установленное время")
        return True
    return False
