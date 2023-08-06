# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Tim C for foamyguy
#
# SPDX-License-Identifier: MIT
"""
`foamyguy_version_testing`
================================================================================

Testing version munging PR


* Author(s): Tim C

Implementation Notes
--------------------


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

changed
"""

# imports
import digitalio
import board

__version__ = "0.0.4"
__repo__ = "https://github.com/foamyguy/Foamyguy_CircuitPython_Version_Testing.git"

the_pin = digitalio.DigitalInOut(board.D1)
