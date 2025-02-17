import logging
import requests
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

CONF_API_URL = "https://api.ownerreservations.com/v2/bookings"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Set up the OwnerRez sensor from a config entry."""
    api_key = entry.data["api_key"]
    async_add_entities([OwnerRezCheckOutSensor(hass, api_key)], True)

class OwnerRezCheckOutSensor(SensorEntity):
    """Sensor for displaying the next OwnerRez Check-out Date."""

    def __init__(self, hass, api_key):
        self.hass = hass
        self._api_key = api_key
        self._attr_name = "OwnerRez Check-out Date"
        self._attr_unique_id = "ownerrez_check_out_date"
        self._state = None
        _LOGGER.debug("✅ OwnerRez Sensor Initialized Successfully!")

    async def async_update(self):
        """Fetch new state data for the sensor."""
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Accept": "application/json"
        }
        params = {
            "include_guest": "true"
        }
        try:
            response = requests.get(CONF_API_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            if data and isinstance(data, list):
                sorted_bookings = sorted(data, key=lambda x: x.get("depart_date"))
                if sorted_bookings:
                    self._state = sorted_bookings[0]["depart_date"]
                else:
                    self._state = "No upcoming check-outs"
            else:
                self._state = "No upcoming check-outs"

        except requests.exceptions.HTTPError as http_err:
            _LOGGER.error(f"HTTP error occurred: {http_err}")
            self._state = "Error"
        except Exception as err:
            _LOGGER.error(f"Other error occurred: {err}")
            self._state = "Error"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return self._attr_unique_id

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._attr_name
