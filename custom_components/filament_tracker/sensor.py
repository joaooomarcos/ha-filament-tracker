"""Sensor entities for Filament Tracker."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant

from .const import DOMAIN

CONF_PRICE = "price"
CONF_COLOR = "color"
CONF_TYPE = "type"


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up filament tracker sensor entities from a config entry."""
    name = config_entry.data[CONF_NAME]
    color = config_entry.data.get(CONF_COLOR, "#FFFFFF")
    price = config_entry.data.get(CONF_PRICE, 0.0)
    filament_type = config_entry.data.get(CONF_TYPE, "PLA")

    entities = [
        FilamentPriceSensor(config_entry.entry_id, name, price),
        FilamentColorSensor(config_entry.entry_id, name, color),
        FilamentTypeSensor(config_entry.entry_id, name, filament_type),
    ]
    async_add_entities(entities)


class FilamentPriceSensor(SensorEntity):
    """Sensor entity for displaying the price (read-only)."""

    def __init__(self, entry_id: str, name: str, price: float) -> None:
        """Initialize the Filament price sensor."""
        self._attr_unique_id = f"{entry_id}_price"
        self._attr_name = f"{name} Price"
        self._attr_native_unit_of_measurement = "R$"
        self._attr_icon = "mdi:currency-brl"
        self._state = price

    @property
    def device_info(self) -> dict:
        """Return device info for grouping entities under one device."""
        config_entry = next(
            (
                entry
                for entry in self.hass.config_entries.async_entries(DOMAIN)
                if entry.entry_id == self._attr_unique_id.split("_", maxsplit=1)[0]
            ),
            None,
        )
        brand = config_entry.data.get("brand", "") if config_entry else ""
        model = config_entry.data.get("model", "") if config_entry else ""
        return {
            "identifiers": {(DOMAIN, self._attr_unique_id.split("_", maxsplit=1)[0])},
            "name": self._attr_name.split(" ", maxsplit=1)[0],
            "manufacturer": brand or "Filament Tracker",
            "model": model or "Generic",
        }

    @property
    def native_value(self) -> float:
        """Return the current price."""
        return self._state


class FilamentColorSensor(SensorEntity):
    """Sensor entity for displaying the color (read-only)."""

    def __init__(self, entry_id: str, name: str, color: str) -> None:
        """Initialize the Filament color sensor."""
        self._attr_unique_id = f"{entry_id}_color"
        self._attr_name = f"{name} Color"
        self._attr_icon = "mdi:palette"
        self._state = color

    @property
    def device_info(self) -> dict:
        """Return device info for grouping entities under one device."""
        config_entry = next(
            (
                entry
                for entry in self.hass.config_entries.async_entries(DOMAIN)
                if entry.entry_id == self._attr_unique_id.split("_", maxsplit=1)[0]
            ),
            None,
        )
        brand = config_entry.data.get("brand", "") if config_entry else ""
        model = config_entry.data.get("model", "") if config_entry else ""
        return {
            "identifiers": {(DOMAIN, self._attr_unique_id.split("_", maxsplit=1)[0])},
            "name": self._attr_name.split(" ", maxsplit=1)[0],
            "manufacturer": brand or "Filament Tracker",
            "model": model or "Generic",
        }

    @property
    def native_value(self) -> str:
        """Return the current color."""
        return self._state


class FilamentTypeSensor(SensorEntity):
    """Sensor entity for displaying the filament type (read-only)."""

    def __init__(self, entry_id: str, name: str, filament_type: str) -> None:
        """Initialize the Filament type sensor."""
        self._attr_unique_id = f"{entry_id}_type"
        self._attr_name = f"{name} Type"
        self._attr_icon = "mdi:format-list-bulleted-type"
        self._state = filament_type

    @property
    def native_value(self) -> str:
        """Return the current filament type."""
        return self._state

    @property
    def device_info(self) -> dict:
        """Return device info for grouping entities under one device."""
        config_entry = next(
            (
                entry
                for entry in self.hass.config_entries.async_entries(DOMAIN)
                if entry.entry_id == self._attr_unique_id.split("_", maxsplit=1)[0]
            ),
            None,
        )
        brand = config_entry.data.get("brand", "") if config_entry else ""
        model = config_entry.data.get("model", "") if config_entry else ""
        return {
            "identifiers": {(DOMAIN, self._attr_unique_id.split("_", maxsplit=1)[0])},
            "name": self._attr_name.split(" ", maxsplit=1)[0],
            "manufacturer": brand or "Filament Tracker",
            "model": model or "Generic",
        }
