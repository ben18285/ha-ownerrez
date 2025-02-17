import logging
import requests
import datetime
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_API_KEY
import voluptuous as vol
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ownerrez"
CONF_API_URL = "https://api.ownerreservations.com/v1/reservations?status=booked"

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.Schema({vol.Required(CONF_API_KEY): cv.string})}, extra=vol.ALLOW_EXTRA
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    api_key = config[CONF_API_KEY]
    add_entities([OwnerRezCheckOutSensor(api_key)], True)

class OwnerRezCheckOutSensor(SensorEntity):
    def __init__(self, api_key):
        self._api_key = api_key
        self._state = None
        self._attr_name = "OwnerRez Check-out Date"
        self.update()

    def update(self):
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
