"""Options flow for Filament Tracker integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.selector import EntitySelector, EntitySelectorConfig

_LOGGER = logging.getLogger(__package__)

AMS_ACTIVE = "ams_active"
USAGE_GRAMS = "usage_grams"
USAGE_METERS = "usage_meters"
AMS_TRAY_1 = "ams_tray_1"
AMS_TRAY_2 = "ams_tray_2"
AMS_TRAY_3 = "ams_tray_3"
AMS_TRAY_4 = "ams_tray_4"


class FilamentTrackerOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle a config options flow for Filament Tracker."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        _LOGGER.info(
            "Options Flow initialized for config entry: %s", config_entry.entry_id
        )
        _LOGGER.debug("Current options: %s", config_entry.options)
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        """Manage the options."""
        _LOGGER.debug("Options Flow Step Init Called")
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = self.config_entry.options

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        USAGE_GRAMS,
                        default=options.get(USAGE_GRAMS, ""),
                    ): EntitySelector(EntitySelectorConfig(domain="sensor")),
                    vol.Required(
                        USAGE_METERS,
                        default=options.get(USAGE_METERS, ""),
                    ): EntitySelector(EntitySelectorConfig(domain="sensor")),
                    vol.Required(
                        AMS_ACTIVE,
                        default=options.get(AMS_ACTIVE, ""),
                    ): EntitySelector(EntitySelectorConfig(domain="binary_sensor")),
                    vol.Required(
                        AMS_TRAY_1,
                        default=options.get(AMS_TRAY_1, ""),
                    ): EntitySelector(EntitySelectorConfig(domain="sensor")),
                    vol.Required(
                        AMS_TRAY_2,
                        default=options.get(AMS_TRAY_2, ""),
                    ): EntitySelector(EntitySelectorConfig(domain="sensor")),
                    vol.Required(
                        AMS_TRAY_3,
                        default=options.get(AMS_TRAY_3, ""),
                    ): EntitySelector(EntitySelectorConfig(domain="sensor")),
                    vol.Required(
                        AMS_TRAY_4,
                        default=options.get(AMS_TRAY_4, ""),
                    ): EntitySelector(EntitySelectorConfig(domain="sensor")),
                }
            ),
        )
