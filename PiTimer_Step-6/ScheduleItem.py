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
#/* PiTimer - Step 6 - User interactions.                                    */
#/* ------------------------------------------------------------------------ */
#/* V1.00 - 2015-07-04 - Jason Birch                                         */
#/* ------------------------------------------------------------------------ */
#/* Class to store a single schedule event in.                               */
#/****************************************************************************/


import operator
import datetime
import SystemTime


# Constants to define relay state.
RELAY_TOGGLE = -1
RELAY_OFF = 0
RELAY_ON = 1


class ScheduleItem:

   def __init__(self, NewRelayNumber, NewScheduleDate, NewRelayState, NewRepeat):
# Unique ID to refer specicially to this specific instance of this class.
      self.ItemID = id(self)
# The ID of the relay this instance referrs to.
      self.RelayNumber = NewRelayNumber
# The time and date this schedule is to activate at.
      self.ScheduleDate = NewScheduleDate
# The state the relay is to be set to.
      self.RelayState = NewRelayState
# The period after activation for the schedule to activate again.
      self.Repeat = NewRepeat


#/****************************************************************/
#/* Return the unique ID of this spacific instance of the class. */
#/****************************************************************/
   def GetItemID(self):
      return self.ItemID


#/*******************************************************************/
#/* Return the relay number of this spacific instance of the class. */
#/*******************************************************************/
   def GetRelayNumber(self):
      return self.RelayNumber


#/*******************************************************************/
#/* Return the relay action of this spacific instance of the class. */
#/*******************************************************************/
   def GetRelayState(self):
      return self.RelayState


#/********************************************************************/
#/* Return the schedule date of this spacific instance of the class. */
#/********************************************************************/
   def GetScheduleDate(self):
      return self.ScheduleDate


#/*******************************************************/
#/* Update the schedule date to the next schedule date. */
#/*******************************************************/
   def SetNextScheduleDate(self):
      Now = datetime.datetime.now()
      if self.Repeat:
         while self.ScheduleDate < Now:
            self.ScheduleDate += self.Repeat
         return True
      else:
         return False


#/**********************************************************************/
#/* When tabulating the results, display a specific row for the table. */
#/**********************************************************************/
   def DisplayItem(self, SelectLeftChar):
      Period = int(self.Repeat.total_seconds())
      Seconds = operator.mod(Period, 60)
      Period = operator.div(Period, 60)
      Minutes = operator.mod(Period, 60)
      Period = operator.div(Period, 60)
      Hours = operator.mod(Period, 24)
      Period = operator.div(Period, 24)
      Days = Period
      print("{}{:^19}".format(SelectLeftChar, self.ScheduleDate.strftime("%Y-%m-%d %H:%M:%S")) + "\r")
      print("{}{:>2}={:<2}  {:>3} {:0>2}:{:0>2}:{:0>2}".format(SelectLeftChar, self.RelayNumber, self.RelayState, str(Days), str(Hours), str(Minutes), str(Seconds)) + "\r")

