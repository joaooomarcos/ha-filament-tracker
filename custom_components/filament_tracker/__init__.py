"""Init file for Filament Tracker integration."""

import logging
from pathlib import Path

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall, callback
import homeassistant.helpers.entity_registry as er
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.typing import ConfigType
from homeassistant.util.json import load_json

from .const import DOMAIN

_LOGGER = logging.getLogger(__package__)

SERVICE_USE_FILAMENT = "use_filament"
LAST_ACTIVE_TRAY_KEY = f"{DOMAIN}_last_active_tray"

SERVICE_SCHEMA = vol.Schema(
    {
        vol.Required("weight"): vol.Coerce(float),
        vol.Required("meters"): vol.Coerce(float),
        vol.Required("color"): str,
    }
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Filament Tracker integration."""
    _LOGGER.debug("Filament Tracker setup called")

    async def load_translations_with_fallback(hass: HomeAssistant, domain, language):
        """Load translations with english fallback."""
        translations = {}

        try:
            translations = await hass.async_add_executor_job(
                load_json,
                Path(hass.config.config_dir)
                / "custom_components"
                / domain
                / "translations"
                / f"{language}.json",
            )
            _LOGGER.debug("Loaded %s translations: %s", language, bool(translations))
        except (FileNotFoundError, ValueError) as e:
            _LOGGER.warning("Failed to load %s translations: %s", language, str(e))

        # English fallback
        if not translations and language != "en":
            try:
                translations = await hass.async_add_executor_job(
                    load_json,
                    Path(hass.config.config_dir)
                    / "custom_components"
                    / domain
                    / "translations"
                    / "en.json",
                )
                _LOGGER.debug(
                    "Loaded English fallback translations: %s", bool(translations)
                )
            except (FileNotFoundError, ValueError) as e:
                _LOGGER.error(
                    "Failed to load English fallback translations: %s", str(e)
                )

        return translations

    async def handle_use_filament(call: ServiceCall) -> None:
        translations = await load_translations_with_fallback(
            hass, DOMAIN, hass.config.language
        )

        weight = call.data["weight"]
        meters = call.data["meters"]
        color = call.data["color"]

        _LOGGER.debug(
            "Service called with weight=%s, meters=%s, color=%s", weight, meters, color
        )

        entity_registry = er.async_get(hass)

        found = False
        for entity_id, entry in entity_registry.entities.items():
            _LOGGER.debug("Checking entity_id: %s, domain: %s", entity_id, entry.domain)
            if entry.domain != "sensor" or not entity_id.endswith("_color"):
                continue

            entry_id_base = entity_id.split(".")[1].rsplit("_", 1)[0]

            color_state = hass.states.get(entity_id)
            _LOGGER.debug(
                "Comparing color for %s: %s == %s",
                entity_id,
                color_state if color_state else None,
                color,
            )

            # Normalize both colors by removing '#' and making lowercase
            def normalize_color(val: str | None) -> str:
                return val.removeprefix("#").lower() if val else ""

            if color_state and normalize_color(color_state.state) == normalize_color(
                color
            ):
                found = True
                weight_entity_id = f"number.{entry_id_base}_weight"
                meters_entity_id = f"number.{entry_id_base}_lenght"
                weight_state = hass.states.get(weight_entity_id)
                meters_state = hass.states.get(meters_entity_id)

                _LOGGER.debug("Found matching filament: %s", entry_id_base)
                _LOGGER.debug("Weight id: %s", weight_entity_id)
                _LOGGER.debug("Lenght id: %s", meters_entity_id)
                _LOGGER.debug("weight_state: %s", weight_state)
                _LOGGER.debug("meters_state: %s", meters_state)

                if weight_state and meters_state:
                    new_weight = max(0, float(weight_state.state) - weight)
                    new_meters = max(0, float(meters_state.state) - meters)
                    _LOGGER.debug(
                        "Setting %s to %s and %s to %s",
                        weight_entity_id,
                        new_weight,
                        meters_entity_id,
                        new_meters,
                    )
                    await hass.services.async_call(
                        "number",
                        "set_value",
                        {"entity_id": weight_entity_id, "value": new_weight},
                        blocking=True,
                    )
                    await hass.services.async_call(
                        "number",
                        "set_value",
                        {"entity_id": meters_entity_id, "value": new_meters},
                        blocking=True,
                    )

                    # Calculate cost and send notification
                    price_entity_id = f"sensor.{entry_id_base}_price"
                    price_state = hass.states.get(price_entity_id)
                    if price_state and price_state.state not in (None, "unknown"):
                        try:
                            price = float(price_state.state)
                            cost = (price / 1000) * weight

                            notification_config = (
                                translations.get("services", {})
                                .get("use_filament", {})
                                .get("notification", {})
                            )

                            title = notification_config.get(
                                "title",
                                "Filament Usage 🧵",  # Fallback padrão
                            )

                            message_template = notification_config.get(
                                "message",
                                "This print used {weight:.2f}g.\nEstimated cost: R$ {cost:.2f}\nRemaining on spool: {new_weight:.2f}g and {new_meters:.2f}m",
                            )

                            # Formata a mensagem
                            try:
                                message = message_template.format(
                                    weight=weight,
                                    cost=cost,
                                    new_weight=new_weight,
                                    new_meters=new_meters,
                                )
                            except KeyError as e:
                                _LOGGER.error("Missing key in translation: %s", str(e))
                                message = f"Print data: {weight}g used, {cost}R$ cost, {new_weight}g remaining"

                            # Envia a notificação
                            await hass.services.async_call(
                                "persistent_notification",
                                "create",
                                {
                                    "title": title,
                                    "message": message,
                                },
                                blocking=True,
                            )
                        except (ValueError, TypeError):
                            _LOGGER.warning(
                                "Could not calculate cost, invalid price value: %s",
                                price_state.state,
                            )
                break
        if not found:
            _LOGGER.warning("No matching filament found for color %s", color)

    hass.services.async_register(
        DOMAIN, SERVICE_USE_FILAMENT, handle_use_filament, schema=SERVICE_SCHEMA
    )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Filament Tracker from a config entry."""
    _LOGGER.debug("Setting up Filament Tracker entry: %s", entry.entry_id)
    entry.async_on_unload(entry.add_update_listener(async_update_options))

    await hass.config_entries.async_forward_entry_setups(entry, ["number", "sensor"])

    # --- AMS status listener ---
    options = entry.options
    ams_status_entity = options.get("ams_active")
    ams_trays = [
        options.get("ams_tray_1"),
        options.get("ams_tray_2"),
        options.get("ams_tray_3"),
        options.get("ams_tray_4"),
    ]
    usage_grams_entity = options.get("usage_grams")
    usage_meters_entity = options.get("usage_meters")

    if (
        ams_status_entity
        and usage_grams_entity
        and usage_meters_entity
        and any(ams_trays)
    ):
        _LOGGER.debug("AMS status")

        @callback
        def _tray_active_listener(event, tray_id):
            """Track last tray that became active."""
            _LOGGER.debug("Tray %s state changed: %s", tray_id, event.data)
            new_state = event.data.get("new_state")
            if new_state and new_state.attributes.get("active") is True:
                _LOGGER.debug("Tray %s is now active", tray_id)
                hass.data[LAST_ACTIVE_TRAY_KEY] = tray_id

        @callback
        def _ams_status_changed(event):
            """Handle AMS status going from on to off."""
            _LOGGER.debug("AMS status changed: %s", event.data)
            old_state = event.data.get("old_state")
            new_state = event.data.get("new_state")
            if not old_state or not new_state:
                return
            if old_state.state == "on" and new_state.state == "off":
                active_tray = hass.data.get(LAST_ACTIVE_TRAY_KEY)
                if not active_tray:
                    _LOGGER.warning("No tray was recently active at AMS shutdown")
                    return
                hass.data.pop(LAST_ACTIVE_TRAY_KEY, None)
                color = hass.states.get(active_tray).attributes.get("color")
                weight = float(hass.states.get(usage_grams_entity).state or 0)
                meters = float(hass.states.get(usage_meters_entity).state or 0)
                _LOGGER.debug(
                    "AMS finished, using filament: color=%s, weight=%s, meters=%s",
                    color,
                    weight,
                    meters,
                )
                hass.async_create_task(
                    hass.services.async_call(
                        DOMAIN,
                        SERVICE_USE_FILAMENT,
                        {
                            "weight": weight,
                            "meters": meters,
                            "color": color,
                        },
                        blocking=True,
                    )
                )

        for tray in ams_trays:
            if tray:
                async_track_state_change_event(
                    hass,
                    [tray],
                    lambda event, tray_id=tray: _tray_active_listener(event, tray_id),
                )

        async_track_state_change_event(hass, [ams_status_entity], _ams_status_changed)

    return True


async def async_update_options(hass: HomeAssistant, config_entry):
    """Update options."""
    await hass.config_entries.async_reload(config_entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_number = await hass.config_entries.async_forward_entry_unload(
        entry, "number"
    )
    unload_sensor = await hass.config_entries.async_forward_entry_unload(
        entry, "sensor"
    )
    return unload_number and unload_sensor
