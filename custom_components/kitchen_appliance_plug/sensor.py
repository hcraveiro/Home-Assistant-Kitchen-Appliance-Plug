from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry
from homeassistant.helpers.device_registry import async_get as async_get_device_registry
from .const import DOMAIN
from .coordinator import KitchenApplianceCoordinator
from .utils import slugify


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: KitchenApplianceCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    entity_registry = async_get_entity_registry(hass)
    device_registry = async_get_device_registry(hass)
    entity_entry = entity_registry.async_get(coordinator.power_sensor)
    device_entry = device_registry.async_get(entity_entry.device_id) if entity_entry else None
    device_identifiers = device_entry.identifiers if device_entry else None

    sensor = KitchenApplianceStatusSensor(
        coordinator=coordinator,
        object_id=slugify(f"{coordinator.name}_status"),
        name=f"{coordinator.name} Status",
        icon=entry.options.get("status_icon", entry.data.get("status_icon", "mdi:chef-hat")),
        device_identifiers=device_identifiers
    )

    async_add_entities([sensor])


class KitchenApplianceStatusSensor(SensorEntity):
    def __init__(self, coordinator, object_id, name, icon, device_identifiers):
        self.coordinator = coordinator
        self._attr_name = name
        self._attr_unique_id = f"kitchen_appliance_{object_id}"
        self._attr_icon = icon
        self._device_identifiers = device_identifiers

    @property
    def native_value(self):
        return self.coordinator.current_state

    @property
    def available(self):
        return self.coordinator.last_update_success

    @property
    def device_info(self):
        if self._device_identifiers:
            return {"identifiers": self._device_identifiers}
        return None

    async def async_update(self):
        await self.coordinator.async_request_refresh()

    async def async_added_to_hass(self):
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
