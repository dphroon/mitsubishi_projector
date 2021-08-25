"""Use serial protocol of Mitsubishi HC6000 projector to obtain state of the projector."""
from __future__ import annotations

import logging
import re
from types import LambdaType
from typing import Any

import serial
import voluptuous as vol
from voluptuous.validators import Boolean

from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchEntity
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

    add_entities([MitsubishiSwitch(serial_port, name, timeout, write_timeout)], True)
    

class MitsubishiSwitch(SwitchEntity):
    """Represents an Mitsubishi HC6000 Projector as a switch."""

    _attr_icon = ICON
    _attr_unique_id = 'switch.mitsubishi_projector'

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
        self._attr_is_on = False ###
        self._serial_port = serial_port
        self._attr_name = name
        self._attributes = {
            LAMP_HOURS: STATE_UNKNOWN,
            INPUT_SOURCE: STATE_UNKNOWN,
            LAMP_MODE: STATE_UNKNOWN,
            SOURCE_AVAIL: STATE_UNKNOWN,
            POWER_AVAIL: STATE_UNKNOWN,
        }

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

    def update(self) -> None:
        """Get the latest state from the projector."""
        awns = self._write_read_format(CMD_DICT[LAMP])
        if awns == "00vP1\r":
            self._attr_is_on = True
            self._attr_available = True
        elif awns == "00vP0\r":
            self._attr_is_on = False
            self._attr_available = True
        else:
#            self._attr_is_on = False
            self._attr_available = True # False

        for key in self._attributes:
            msg = CMD_DICT.get(key)
            if msg:
                awns = self._write_read_format(msg)
                #if key == LAMP_HOURS:
                #    awns = self._write_read_format(msg)
                #    self._attributes[key] = awns
                if key == LAMP_HOURS:
                    awns = (awns[5:9] + " hours", awns[9:11] + " minutes")#self._write_read_format(msg)
                elif key == POWER_AVAIL:
                    if awns == "00vPK0\r":
                        awns = "Unavailable"
                    elif awns == "00vPK1\r":
                        awns = "Available"
                    else:
                        awns = self._attributes[key]
                elif key == SOURCE_AVAIL:
                    if awns == "00vSM0\r":
                        awns = "Unavailable"
                    elif awns == "00vSM1\r":
                        awns = "Available"
                    else:
                        awns = self._attributes[key]
                elif key == INPUT_SOURCE:
                    if awns == "00vIr1\r":
                        awns = "Computer"
                    elif awns == "00vIc1\r":
                        awns = "Component"
                    elif awns == "00vId1\r":
                        awns = "HDMI 1"
                    elif awns == "00vId2\r":
                        awns = "HDMI 2"
                    elif awns == "00vIv1\r":
                        awns = "Video"
                    elif awns == "00vIv2\r":
                        awns = "S-Video"
                    else:
                        awns = self._attributes[key]
                elif key == LAMP_MODE:
                    if awns == "00LM1\r":
                        awns = "Low"
                    elif awns == "00LM0\r":
                        awns = "Normal"
                    else:
                        awns = self._attributes[key]
                else:
                    #awns = self._write_read_format(msg)
                    self._attributes[key] = awns               
                #awns = self._write_read_format(msg)
                self._attributes[key] = awns
        self._attr_extra_state_attributes = self._attributes

    def turn_on(self, **kwargs: Any) -> None:
        """Turn the projector on."""
        msg = CMD_DICT[STATE_ON]
        self._write_read(msg)
        self._attr_is_on = True

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the projector off."""
        msg = CMD_DICT[STATE_OFF]
        self._write_read(msg)
        self._attr_is_on = False

