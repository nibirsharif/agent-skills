"""The status light on the front panel of the NAS."""

from pathlib import Path

LIGHT = Path("/sys/class/leds/nas:status/color")


def set_light(colour):
    """Set the status light: green, amber, or red. Does nothing on a machine without the panel."""
    if LIGHT.exists():
        LIGHT.write_text(colour)
