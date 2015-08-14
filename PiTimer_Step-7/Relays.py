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
#/* PiTimer - Step 7 - Save/Load application state.                          */
#/* ------------------------------------------------------------------------ */
#/* V1.00 - 2015-07-04 - Jason Birch                                         */
#/* ------------------------------------------------------------------------ */
#/* Class to handle the current relay states.                                */
#/****************************************************************************/


import operator
import datetime
import SystemTime


# Constants to define relay state.
RELAY_OFF = 0
RELAY_ON = 1


class Relays:

   def __init__(self):
# Instance storage for relay states.
      self.RelayState = []


#/***********************************************************/
#/* Add a relay to the relays supported by the application. */
#/***********************************************************/
   def AddRelay(self, RelayNumber, RelayState):
      self.RelayState.append([RelayNumber, RelayState])


#/*******************************************/
#/* Display a table of the current relay    */
#/* states and the date/time at that point. */
#/*******************************************/
   def DisplayRelayStates(self):
      ThisSystemTime = SystemTime.SystemTime()
      print("{:>20}".format(ThisSystemTime.SystemTimeString()) + "\r")
      Line1 = ""
      Line2 = ""
      Line3 = ""
      for ThisRelayState in self.RelayState:
         if ThisRelayState[0]:
            RelayDiv = operator.div(ThisRelayState[0], 10)
            RelayMod = operator.mod(ThisRelayState[0], 10)
            if RelayDiv:
               Line1 += str(RelayDiv)
            else:
               Line1 += " "
            Line2 += str(RelayMod)
            Line3 += str(ThisRelayState[1])
      print(Line1 + "\r")
      print(Line2 + "\r")
      print(Line3 + "\r")


#/************************************************/
#/* Get the current state of the specific relay. */
#/************************************************/
   def GetRelayState(self, RelayNumber):
      Result = False
      if RelayNumber - 1 < len(self.RelayState):
         Result = self.RelayState[RelayNumber][1]
      return Result


#/************************************************/
#/* Set the current state of the specific relay. */
#/************************************************/
   def SetRelayState(self, RelayNumber, NewRelayState):
      if RelayNumber - 1 < len(self.RelayState):
         self.RelayState[RelayNumber - 1][1] = NewRelayState


#/***************************************************/
#/* Toggle the current state of the specific relay. */
#/***************************************************/
   def ToggleRelayState(self, RelayNumber):
      Result = False
      if RelayNumber - 1 < len(self.RelayState):
         if self.RelayState[RelayNumber - 1][1] == RELAY_OFF:
            self.RelayState[RelayNumber - 1][1] = RELAY_ON
         else:
            self.RelayState[RelayNumber - 1][1] = RELAY_OFF
         Result = self.RelayState[RelayNumber - 1][1]
      return Result

