"""Number entities for Filament Tracker."""

from homeassistant.components.number import NumberEntity
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.restore_state import RestoreEntity

from .const import DOMAIN, SENSOR_TYPES

CONF_INITIAL_LENGTH = "initial_length"
CONF_INITIAL_WEIGHT = "initial_weight"


async def async_setup_entry(
    hass: HomeAssistant, config_entry, async_add_entities
) -> None:
    """Set up filament tracker number entities from a config entry."""
    name = config_entry.data[CONF_NAME]
    initial_lenght = config_entry.data.get(CONF_INITIAL_LENGTH, 0.0)
    initial_weight = config_entry.data.get(CONF_INITIAL_WEIGHT, 0.0)

    entities = [
        FilamentNumberEntity(config_entry.entry_id, name, "lenght", initial_lenght),
        FilamentNumberEntity(config_entry.entry_id, name, "weight", initial_weight),
    ]
    async_add_entities(entities)


class FilamentNumberEntity(NumberEntity, RestoreEntity):
    """Number entity for tracking filament properties."""

    def __init__(
        self, entry_id: str, name: str, number_type: str, initial_value: float
    ) -> None:
        """Initialize the Filament number entity."""
        self._attr_unique_id = f"{entry_id}_{number_type}"
        self._attr_name = f"{name} {SENSOR_TYPES[number_type][0]}"
        self._attr_native_unit_of_measurement = SENSOR_TYPES[number_type][1]
        self._attr_icon = SENSOR_TYPES[number_type][2]
        self._attr_native_min_value = 0.0
        self._attr_native_max_value = 100000.0
        self._attr_native_step = 0.01
        self._state = initial_value

    @property
    def native_value(self) -> float:
        """Return the current value."""
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

    async def async_set_native_value(self, value: float) -> None:
        """Set a new value."""
        self._state = value
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Restore previous state after Home Assistant restart."""
        if (
            last_state := await self.async_get_last_state()
        ) is not None and last_state.state not in (None, "unknown"):
            try:
                self._state = float(last_state.state)
            except (ValueError, TypeError):
                self._state = self._state
