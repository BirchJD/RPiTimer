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
#/* PiTimer - Step 3 - Schedule table.                                       */
#/* ------------------------------------------------------------------------ */
#/* V1.00 - 2015-07-04 - Jason Birch                                         */
#/* ------------------------------------------------------------------------ */
#/* Class to handle scheduling events for specific relays. Such as adding,   */
#/* removing, displaying, sorting.                                           */
#/****************************************************************************/


import ScheduleItem


class Schedule:

   def __init__(self):
# Define an array to store the schedule items in.
      self.ScheduleItems = []


#/*********************************************/
#/* Get the item at the specific array index. */
#/*********************************************/
   def GetItem(self, ItemIndex):
      if len(self.ScheduleItems) > ItemIndex:
         return self.ScheduleItems[ItemIndex]
      else:
         return False


#/*******************************************************/
#/* Function to display the current schedule of events. */
#/* In a tabulated form.                                */
#/*******************************************************/
   def DisplaySchedule(self, SelectedItemID):
      if len(self.ScheduleItems):
         self.ScheduleItems[0].DisplayHeader()

      for ThisScheduleItem in self.ScheduleItems:
         if SelectedItemID == ThisScheduleItem.GetItemID():
            SelectLeftChar = ">"
            SelectRightChar = "<"
         else:
            SelectLeftChar = " "
            SelectRightChar = " "
         ThisScheduleItem.DisplayItem(SelectLeftChar, SelectRightChar)

      if len(self.ScheduleItems):
         self.ScheduleItems[0].DisplayFooter()


#/*************************************************/
#/* Add a new schedule item to the schedle array. */
#/*************************************************/
   def AddSchedule(self, NewRelayNumber, NewScheduleDate, NewRelayState, NewRepeat):
      self.ScheduleItems.append(ScheduleItem.ScheduleItem(NewRelayNumber, NewScheduleDate, NewRelayState, NewRepeat))

