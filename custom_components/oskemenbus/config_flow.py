"""Config flow for Oskemen Bus integration."""
from __future__ import annotations

from typing import Any

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

class OskemenBusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Oskemen Bus."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_NAME, default="Oskemen Bus"): str,
                    }
                ),
            )

        return self.async_create_entry(
            title=user_input[CONF_NAME],
            data=user_input,
        )