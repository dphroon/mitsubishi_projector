# A Home Assistant custom Integration for serial control of Mitsubishi HC6000 LCD Projectors.

The following device infromation is polled:
* Power state (ON/OFF)
* Lamp use in hours and minutes. This is calculated in Low mode
* Lamp Mode
* Current Source
* Signal presence of current source
* Power state change availability

After the device is switched on or off, there is a device based block on changing the state again (manufacturer documents 10 seconds, but may be longer) . Power state change polls this.

# Installation:

Copy the mitsubishi_projector folder and all of its contents into your Home Assistant's custom_components folder. This is often located inside of your /config folder. If you are running Hass.io, use SAMBA to copy the folder over. If you are running Home Assistant Supervised, the custom_components folder might be located at /usr/share/hassio/homeassistant. It is possible that your custom_components folder does not exist. If that is the case, create the folder in the proper location, and then copy the mitsubishi_projector folder and all of its contents inside the newly created custom_components folder.

Alternatively, you can install mitsubishi_projector through HACS by adding this repository.


# Configuration:

Add the proper entry to your configuration.yaml file. Several example configurations for different device types are provided below. Make sure to save when you are finished editing configuration.yaml.

```
switch:
  - platform: mitsubishi_projector
    filename: /dev/ttyUSB0                      # Required (device). The pipe where the projector is connected to.
    name: "Mitsubishi HC6000 LCD Projector"     # Optional (string). The displayed name of the switch.
    timeout: 1                                  # Optional (integer). Time to wait for serial read in seconds
    write_timeout: 1

```

* filename (string) **Required**
** _The pipe where the projector is connected to. Use dev-by-id to prevent USB changes affecting this._
* name (string) (Optional)
** _The name to use when displaying this switch._
* timeout (integer) (Optional)
** _Timeout for the connection in seconds._
* write_timeout (integer) (Optional)
** _Write timeout in seconds._



Restart Home Assistant when finished editing.


# To-do list:

* Create a Device and add other functions available
   

