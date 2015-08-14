# PiTimer - Python Hardware Programming Education Project For Raspberry Pi
# Copyright (C) 2015 Jason Birch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#/****************************************************************************/
#/* PiTimer - Step 10 - Numeric GPIO keypad.                                 */
#/* ------------------------------------------------------------------------ */
#/* V1.00 - 2015-07-04 - Jason Birch                                         */
#/* ------------------------------------------------------------------------ */
#/* Class to handle reading key codes from a keypad connected to GPIO pins.  */
#/****************************************************************************/


import RPi.GPIO


class Keypad:

   def __init__(self, GpioPins):
# Store GPIO pins used for Keypad.
      self.ThisGpioPins = GpioPins
# Last key code pressed.
      self.LastKeyCode = -1
# Prevent double reads of the same keypress.
      self.DebounceKey = -1
# GPIO matrix to keycode lookup.
      self.KeyCodeLookup = [ ord("1"), ord("2"), ord("3"),
                             ord("4"), ord("5"), ord("6"),
                             ord("7"), ord("8"), ord("9"),
                             ord("*"), ord("0"), ord("#") ]


# Setup the GPIO for a 4 x 3 keypad matrix. 4 output and 3 input,
# as the 4 output can be uesed to drive data to a 20x4 LCD display too.
      for Count in range(0, len(self.ThisGpioPins)):
         if Count < 3:
            RPi.GPIO.setup(self.ThisGpioPins[Count], RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
         else:
            RPi.GPIO.setup(self.ThisGpioPins[Count], RPi.GPIO.OUT, initial=1)


#/************************************/
#/* Scan the keypad for key presses. */
#/************************************/
   def ScanKeypad(self):
# Don't scan the keypad until the last key has been read.
      if self.LastKeyCode == -1:
# Make sure all keypad output lines are high to start.
         for Row in range(3, 7):
            RPi.GPIO.output(self.ThisGpioPins[Row], 1)

# Scan the keypad for key presses, taking the output lines down one at a time.
         KeyCode = -1
         Count = 0
         for Row in range(3, 7):
            RPi.GPIO.output(self.ThisGpioPins[Row], 0)
            for Col in range(0, 3):
               if RPi.GPIO.input(self.ThisGpioPins[Col]) == 0:
                  KeyCode = self.KeyCodeLookup[Count]
               Count = Count + 1
            RPi.GPIO.output(self.ThisGpioPins[Row], 1)
         if KeyCode != self.DebounceKey:
            self.LastKeyCode = KeyCode


#/***********************************************/
#/* Return the keycode of the last key presses. */
#/************************************************/
   def GetKeyCode(self):
      Result =  self.LastKeyCode
      self.DebounceKey = self.LastKeyCode
      self.LastKeyCode = -1
      return Result

