"""Use serial protocol of Mitsubishi HC6000 projector to obtain state of the projector."""
from __future__ import annotations

import logging
from os import name
import re
from types import LambdaType
from typing import Any

import serial
import voluptuous as vol
from voluptuous.validators import Boolean

from homeassistant.components.select import PLATFORM_SCHEMA, SelectEntity
from homeassistant.const import (
    CONF_FILENAME,
    CONF_NAME,
    CONF_TIMEOUT,
    STATE_OFF,
    STATE_ON,
    STATE_UNKNOWN,
)
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
    CMD_DICT,
    CONF_WRITE_TIMEOUT,
    DEFAULT_NAME,
    DEFAULT_TIMEOUT,
    DEFAULT_WRITE_TIMEOUT,
    LAMP_MODE,
    ICON,
    SOURCE_ICON,
    INPUT_SOURCE,
    LAMP,
    LAMP_HOURS,
    SOURCE_AVAIL,
    POWER_AVAIL,
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_FILENAME): cv.isdevice,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int,
        vol.Optional(
            CONF_WRITE_TIMEOUT, default=DEFAULT_WRITE_TIMEOUT
        ): cv.positive_int,
    }
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType,
) -> None:
    """Connect with serial port and return Mitsubishi HC6000 Projector."""
    serial_port = config[CONF_FILENAME]
    name = config[CONF_NAME]
    timeout = config[CONF_TIMEOUT]
    write_timeout = config[CONF_WRITE_TIMEOUT]

    add_entities([MitsubishiInputSelect(serial_port, name, timeout, write_timeout)], True)

class MitsubishiInputSelect(SelectEntity):

    _attr_icon = SOURCE_ICON
    _attr_unique_id = 'select.mitsubishi_projector_input'

    def __init__(
        self,
        serial_port: str,
        name: str,
        timeout: int,
        write_timeout: int,
    ) -> None:
        """Init of the Mitsubishi HC6000 projector."""
        self.ser = serial.Serial(
            port=serial_port, timeout=timeout, write_timeout=write_timeout,
        )
        self._serial_port = serial_port
        self._attr_name = name + '_source'
        self._attr_options = [
            "Computer",
            "Component",
            "HDMI 1",
            "HDMI 2",
            "Video",
            "S-Video"
        ]
        # self._attr_current_option = 

    def _write_read(self, msg: str) -> str:
        """Write to the projector and read the return."""
        ret = ""
        # Sometimes the projector won't answer for no reason or the projector
        # was disconnected during runtime.
        # This way the projector can be reconnected and will still work
        try:
            if not self.ser.is_open:
                self.ser.open()
            self.ser.write(msg.encode("utf-8"))
            # Size is an experience value there is no real limit.
            # AFAIK there is no limit and no end character so we will usually
            # need to wait for timeout
            ret = self.ser.read_until(size=20).decode("utf-8")
        except serial.SerialException:
            _LOGGER.error("Problem communicating with %s", self._serial_port)
        self.ser.close()
        return ret
###
    def _write_read_format(self, msg: str) -> str:
        """Write msg, obtain answer and format output."""
        # answers are formatted as answer\r
        awns = self._write_read(msg)
        match = re.search(r"\r(.+)\r", awns)
        if match:
            return match.group(1)
        return awns #STATE_UNKNOWN

    def current_option(self) -> None:
        awns = "HDMI 1"
        return awns

    def select_option(self, selection: str) -> None:
        msg = CMD_DICT[selection]
        self._write_read(msg)
        return
