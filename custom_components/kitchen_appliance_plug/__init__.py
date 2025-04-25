"""Kitchen Appliance Plug integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
import logging

from .const import (
    DOMAIN,
    CONF_POWER_SENSOR,
    CONF_MINIMUM_POWER,
    CONF_ACTIVE_STATE_NAME,
    CONF_IDLE_DELAY,
    DEFAULT_IDLE_DELAY
)
from .coordinator import KitchenApplianceCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Kitchen Appliance Plug from a config entry."""

    data = {
        **config_entry.data,
        **config_entry.options,
        "name": config_entry.title,
    }

    idle_delay = data.get(CONF_IDLE_DELAY, DEFAULT_IDLE_DELAY)

    coordinator = KitchenApplianceCoordinator(
        hass,
        name=data["name"],
        power_sensor=data[CONF_POWER_SENSOR],
        min_power=data[CONF_MINIMUM_POWER],
        active_state=data[CONF_ACTIVE_STATE_NAME],
        idle_delay=idle_delay,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = {
        "coordinator": coordinator,
    }

    config_entry.async_on_unload(config_entry.add_update_listener(update_listener))

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(config_entry.entry_id)
    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Força o reload da config entry quando as opções são atualizadas."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_get_options_flow(config_entry: ConfigEntry):
    _LOGGER.debug("✅ async_get_options_flow invocado")
    from .config_flow import async_get_options_flow
    return async_get_options_flow(config_entry)
