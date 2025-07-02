"""Config flow for Filament Tracker integration."""

import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import callback

from .const import DOMAIN
from .options_flow import FilamentTrackerOptionsFlowHandler

CONF_COLOR = "color"
CONF_INITIAL_LENGTH = "initial_length"
CONF_INITIAL_WEIGHT = "initial_weight"
CONF_PRICE = "price"
CONF_BRAND = "brand"
CONF_TYPE = "type"
CONF_MODEL = "model"

FILAMENT_TYPES = ["PLA", "PETG", "ABS"]

_LOGGER = logging.getLogger(__package__)


class FilamentConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Filament Tracker."""

    VERSION = 1
    supports_options = True

    @staticmethod
    @callback
    def async_get_options_flow(config_entry) -> FilamentTrackerOptionsFlowHandler:
        """Create the options flow."""
        _LOGGER.debug("Options Flow")
        return FilamentTrackerOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle the initial step of the config flow for user input."""
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_NAME,
                        description={
                            "suggested_value": "Filamento Azul",
                        },
                    ): str,
                    vol.Required(
                        CONF_COLOR,
                        description={
                            "suggested_value": "#FFFFFFFF",
                        },
                    ): str,
                    vol.Optional(
                        CONF_INITIAL_LENGTH,
                        default=330.0,
                        description={
                            "suggested_value": "330.0",
                        },
                    ): vol.Coerce(float),
                    vol.Optional(
                        CONF_INITIAL_WEIGHT,
                        default=1000.0,
                        description={
                            "suggested_value": "1000.0",
                        },
                    ): vol.Coerce(float),
                    vol.Optional(
                        CONF_PRICE,
                        default=100.0,
                        description={
                            "suggested_value": "100.0",
                        },
                    ): vol.Coerce(float),
                    vol.Required(
                        CONF_TYPE,
                        default="PLA",
                    ): vol.In(FILAMENT_TYPES),
                    vol.Optional(
                        CONF_BRAND,
                        default="",
                        description={
                            "suggested_value": "Generic",
                        },
                    ): str,
                    vol.Optional(
                        CONF_MODEL,
                        default="",
                        description={
                            "suggested_value": "Generic",
                        },
                    ): str,
                }
            ),
        )
