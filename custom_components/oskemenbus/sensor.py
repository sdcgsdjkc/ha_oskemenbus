"""Support for Oskemen Bus sensors."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Oskemen Bus sensor."""
    async_add_entities([OskemenBusSensor(entry)], True)

class OskemenBusSensor(SensorEntity):
    """Representation of an Oskemen Bus sensor."""

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self._attr_unique_id = f"{entry.entry_id}"
        self._attr_name = entry.title
        self._attr_native_value = None

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        # Implement the bus data fetching logic here
        pass