from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers.selector import selector
import voluptuous as vol

from .const import (
    DOMAIN,
    CONF_POWER_SENSOR,
    CONF_MINIMUM_POWER,
    CONF_ACTIVE_STATE_NAME,
    DEFAULT_MINIMUM_POWER,
    DEFAULT_NAME,
    CONF_IDLE_DELAY,
    DEFAULT_IDLE_DELAY,
)

CONF_STATUS_ICON = "status_icon"
DEFAULT_ICON = "mdi:chef-hat"


class KitchenAppliancePlugConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return KitchenAppliancePlugOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Required(CONF_POWER_SENSOR): selector({
                    "entity": {
                        "domain": "sensor",
                        "device_class": "power"
                    }
                }),
                vol.Required(CONF_MINIMUM_POWER, default=DEFAULT_MINIMUM_POWER): selector({
                    "number": {
                        "min": 0,
                        "max": 10000,
                        "step": 0.1,
                        "unit_of_measurement": "W",
                        "mode": "box"
                    }
                }),
                vol.Required(CONF_IDLE_DELAY, default=DEFAULT_IDLE_DELAY): selector({
                    "number": {
                        "min": 5,
                        "max": 1800,
                        "step": 5,
                        "unit_of_measurement": "s",
                        "mode": "box"
                    }
                }),
                vol.Required(CONF_ACTIVE_STATE_NAME, default="Cooking"): str,
                vol.Required(CONF_STATUS_ICON, default=DEFAULT_ICON): selector({
                    "icon": {}
                }),
            }),
        )


class KitchenAppliancePlugOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_MINIMUM_POWER, default=self.config_entry.options.get(
                    CONF_MINIMUM_POWER, self.config_entry.data.get(CONF_MINIMUM_POWER, DEFAULT_MINIMUM_POWER)
                )): selector({
                    "number": {
                        "min": 0,
                        "max": 10000,
                        "step": 0.1,
                        "unit_of_measurement": "W",
                        "mode": "box"
                    }
                }),
                vol.Required(CONF_IDLE_DELAY, default=DEFAULT_IDLE_DELAY): selector({
                    "number": {
                        "min": 5,
                        "max": 1800,
                        "step": 5,
                        "unit_of_measurement": "s",
                        "mode": "box"
                    }
                }),
                vol.Required(CONF_ACTIVE_STATE_NAME, default=self.config_entry.options.get(
                    CONF_ACTIVE_STATE_NAME, self.config_entry.data.get(CONF_ACTIVE_STATE_NAME, "Cooking")
                )): str,
                vol.Required(CONF_STATUS_ICON, default=self.config_entry.options.get(
                    CONF_STATUS_ICON, self.config_entry.data.get(CONF_STATUS_ICON, DEFAULT_ICON)
                )): selector({
                    "icon": {}
                }),
            }),
        )
