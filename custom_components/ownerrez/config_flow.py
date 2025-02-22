import logging
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class OwnerRezConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for OwnerRez integration."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="OwnerRez", data={"api_key": user_input["api_key"]})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required("api_key"): str}),
            errors=errors,
        )
