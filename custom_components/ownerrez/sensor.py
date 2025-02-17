import logging
import requests
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

CONF_API_URL = "https://api.ownerreservations.com/v1/reservations?status=booked"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Set up the OwnerRez sensor from a config entry."""
    api_key = entry.data["api_key"]
    async_add_entities([OwnerRezCheckOutSensor(hass, api_key)], True)

class OwnerRezCheckOutSensor(SensorEntity):
    """Sensor for displaying the next OwnerRez check-out date."""

    def __init__(self, hass, api_key):
        self.hass = hass
        self._api_key = api_key
        self._attr_name = "OwnerRez Check-out Date"
        self._attr_unique_id = "ownerrez_check_out_date"
        self._state = None

    async def async_update(self):
        """Fetch new state data for the sensor."""
        headers = {"Authorization": f"Bearer {self._api_key}", "Accept": "application/json"}
        try:
            response = requests.get(CONF_API_URL, headers=headers)
            data = response.json()
            if "reservations" in data and len(data["reservations"]) > 0:
                self._state = data["reservations"][0]["depart_date"]
            else:
                self._state = "No upcoming check-outs"
        except Exception as e:
            _LOGGER.error(f"Error fetching OwnerRez data: {e}")
            self._state = "Error"

    @property
    def state(self):
        return self._state

    @property
    def unique_id(self):
        return "ownerrez_check_out_date"
