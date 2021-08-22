"""Use serial protocol of Acer projector to obtain state of the projector."""
from __future__ import annotations

from typing import Final

from homeassistant.const import STATE_OFF, STATE_ON

CONF_WRITE_TIMEOUT: Final = "write_timeout"

DEFAULT_NAME: Final = "Mitsubishi Projector"
DEFAULT_TIMEOUT: Final = 1
DEFAULT_WRITE_TIMEOUT: Final = 1

LAMP_MODE: Final = "Lamp Mode"

ICON: Final = "mdi:projector"

INPUT_SOURCE: Final = "Input Source"

SOURCE_AVAIL: Final = "Source Signal"
POWER_AVAIL: Final = "Power Switching"

LAMP: Final = "Lamp"
LAMP_HOURS: Final = "Lamp Hours"

MODEL: Final = "Model"

# Commands known to the projector
CMD_DICT: Final[dict[str, str]] = {
    LAMP: "00vP\r",
    LAMP_HOURS: "00vLE\r",
    INPUT_SOURCE: "00vI\r",
    SOURCE_AVAIL: "00vSM\r",
    POWER_AVAIL: "00vPK\r",
    LAMP_MODE: "00LM\r",
    MODEL: "00LM\r",
    STATE_ON: "00!\r",
    STATE_OFF: "00\"\r"
}
