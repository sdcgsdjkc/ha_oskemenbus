import sys
import asyncio
import logging
from homeassistant import config_entries

DOMAIN = "oskemenbus"
_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    return True

async def async_setup_entry(hass, entry):
    # Формируем путь к main.py, который находится в подпапке oskemenbus_parser
    script_path = hass.config.path("custom_components", DOMAIN, "oskemenbus_parser", "main.py")
    
    _LOGGER.info("Запуск FastAPI-сервера из %s", script_path)
    try:
        process = await asyncio.create_subprocess_exec(
            sys.executable, script_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        hass.data.setdefault(DOMAIN, {})[entry.entry_id] = process
    except Exception as e:
        _LOGGER.error("Ошибка запуска FastAPI-сервера: %s", e)
        return False

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True

async def async_unload_entry(hass, entry):
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
