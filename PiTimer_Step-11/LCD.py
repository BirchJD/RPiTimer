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
#/* PiTimer - Step 11 - 20 x 4 LCD display.                                  */
#/* ------------------------------------------------------------------------ */
#/* V1.00 - 2015-07-04 - Jason Birch                                         */
#/* ------------------------------------------------------------------------ */
#/* Class to handle writing to an LCD module, connected to GPIO pins.        */
#/****************************************************************************/


import operator
import RPi.GPIO


# GPIO array LCD pin indexes.
LCD_RS_PIN = 0
LCD_E_PIN = 1
LCD_D4_PIN = 2
LCD_D5_PIN = 3
LCD_D6_PIN = 4
LCD_D7_PIN = 5
# LCD module start of line addresses.
CURSOR_LINE_POS = [ 0, 64, 20, 84 ]


class LCD:

   def __init__(self, GpioPins):
# Store GPIO pins used for LCD.
      self.ThisGpioPins = GpioPins
# Text line comparison cache.
      self.TextLineCache = [ "", "", "", "" ]
# Data nibble cache, queue data here to go to the LCD display.
      self.NibbleCache = []
# Rememver the state of the E clock pin.
      self.ePinFlag = False
# Configure all GPIO pins to output.
      for Count in range(len(self.ThisGpioPins)):
         RPi.GPIO.setup(self.ThisGpioPins[Count], RPi.GPIO.OUT, initial=0)
# Initialise display 4bit operation.
      self.CacheNibble(int("0010", 2), False)
# Set display lines to 2, which is required for a 4 line display.
      self.CacheByte(int("00101000", 2), False)
# Set display on, cursor off.
      self.CacheByte(int("00001100", 2), False)
# Set display cursor move write after character write.
      self.CacheByte(int("00000110", 2), False)


#/***********************************************************/
#/* Allow other devices to check if the GPIO pins are busy. */
#/* So they can use the same GPIO pins for another purpose. */
#/***********************************************************/
   def IsBusy(self):
      return self.ePinFlag or len(self.NibbleCache)


#/**************************************/
#/* Set clear dispaly and cursor home. */
#/**************************************/
   def Clear(self):
      self.CacheByte(int("00000001", 2), False)


#/********************/
#/* Set cursor home. */
#/********************/
   def Home(self):
      self.CacheByte(int("00000010", 2), False)


#/***********************************************/
#/* Set the cursor position to the LCD address. */
#/***********************************************/
   def SetCursorPos(self, Pos):
      self.CacheByte(int("10000000", 2) + (Pos & int("7F", 16)), False)


#/***************************************************/
#/* Write a line of text to the specified LCD line. */
#/***************************************************/
   def CacheLine(self, LineNumber, Text):
      CursorPos = CURSOR_LINE_POS[LineNumber - 1]
      Count = 0
      SetPos = True
      for Char in Text:
         if len(self.TextLineCache[LineNumber - 1]) <= Count or Char != self.TextLineCache[LineNumber - 1][Count]:
            if SetPos == True:
               SetPos = False
               self.SetCursorPos(CursorPos)
            self.CacheChr(Char)
         else:
            SetPos = True
         CursorPos += 1
         Count += 1
      self.TextLineCache[LineNumber - 1] = Text


#/***********************************************/
#/* Write an ASCII character to the LCD module. */
#/***********************************************/
   def CacheChr(self, Char):
      self.CacheByte(ord(Char), True)


#/*********************************************************************/
#/* Write a byte of data to the specified register of the LCD module. */
#/*********************************************************************/
   def CacheByte(self, Byte, RsFlag):
      HighNibble = operator.div(Byte, 16)
      LowNibble = operator.mod(Byte, 16)
      self.CacheNibble(HighNibble, RsFlag)
      self.CacheNibble(LowNibble, RsFlag)


#/***************************************************************************/
#/* Main application adds data to be sent to the LCD here. The data is sent */
#/* to the LCD when the LCD is ready to process data and does not hold up   */
#/* the main application processing. Bit 0-3 Data, bit 4 RS line.           */
#/***************************************************************************/
   def CacheNibble(self, Nibble, RsFlag):
      if RsFlag:
         Nibble |= int("10000", 2)
      self.NibbleCache.append(Nibble)


#/************************************************************************/
#/* Called from main application loop every 5ms, in order to write data */
#/* to the LCD at a rate slow enough for the LCD to handle.              */
#/************************************************************************/
   def WriteNibble(self):
      if self.ePinFlag:
         self.ePinFlag = False
# Finish clocking the previous data into the LCD module.
         RPi.GPIO.output(self.ThisGpioPins[LCD_E_PIN], 0)
      elif len(self.NibbleCache):
# Start to clock the data into the LCD module.
         self.ePinFlag = True
         RPi.GPIO.output(self.ThisGpioPins[LCD_E_PIN], 1)
# Get the next data to send from the LCD cache.
         Nibble = self.NibbleCache.pop(0)
# Bit 4 of the cache data item is the RS line data.
         if Nibble & int("10000", 2):
            Bit = 1
         else:
            Bit = 0
         RPi.GPIO.output(self.ThisGpioPins[LCD_RS_PIN], Bit)
# Bits 0-3 of the cache data item is the 4 bit data nibble.
         for Count in range(4):
            Bit = operator.mod(Nibble, 2)
            Nibble = operator.div(Nibble, 2)
            RPi.GPIO.output(self.ThisGpioPins[Count + 2], Bit)

