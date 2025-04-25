from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.util import dt as dt_util
import logging

_LOGGER = logging.getLogger(__name__)


class KitchenApplianceCoordinator(DataUpdateCoordinator):
    def __init__(
        self,
        hass: HomeAssistant,
        name: str,
        power_sensor: str,
        min_power: float,
        active_state: str,
        idle_delay: int,
    ):
        super().__init__(
            hass,
            _LOGGER,
            name=name,
            update_interval=timedelta(seconds=15),
        )
        self.power_sensor = power_sensor
        self.min_power = min_power
        self.active_state = active_state
        self.idle_delay = idle_delay  # em segundos
        self.current_state = "Off"
        self._below_threshold_since = None

    async def _async_update_data(self):
        power_state = self.hass.states.get(self.power_sensor)

        if power_state is None or power_state.state in (STATE_UNAVAILABLE, "unknown"):
            self.current_state = "Off"
            self._below_threshold_since = None
            return

        try:
            power = float(power_state.state)

            if power >= self.min_power:
                self.current_state = self.active_state
                self._below_threshold_since = None

            else:
                now = dt_util.now()
                if self._below_threshold_since is None:
                    self._below_threshold_since = now
                    self.current_state = self.active_state  # ainda a contar tempo
                elif (now - self._below_threshold_since).total_seconds() >= self.idle_delay:
                    self.current_state = "Off"
                else:
                    self.current_state = self.active_state  # ainda dentro do delay

        except ValueError:
            self.current_state = "Off"
            self._below_threshold_since = None
