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
SOURCE_ICON: Final = "mdi:video-input-hdmi"

INPUT_SOURCE: Final = "Input Source"

SOURCE_AVAIL: Final = "Source Signal"
POWER_AVAIL: Final = "Power Switching"

LAMP: Final = "Lamp"
LAMP_HOURS: Final = "Lamp Hours"
INPUT_HDMI1: Final = "HDMI 1"
INPUT_HDMI2: Final = "HDMI 2"
INPUT_PC: Final = "Computer"
INPUT_COMP: Final = "Component"
INPUT_VIDEO: Final = "Video"
INPUT_SVIDEO: Final = "S-Video"
    
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
    STATE_OFF: "00\"\r",
    INPUT_HDMI1: "00_d1\r",
    INPUT_HDMI2: "00_d2\r",
    INPUT_PC: "00_r1\r",
    INPUT_COMP: "00_c1\r",
    INPUT_VIDEO: "00_v1\r",
    INPUT_SVIDEO:"00_v2\r" 
}
