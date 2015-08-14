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
#/* Class to handle scheduling events for specific relays. Such as adding,   */
#/* removing, displaying, sorting.                                           */
#/****************************************************************************/


import datetime
import ScheduleItem


#/****************************************************************************/
#/* Function to return the schedule date of a schedule item for when sorting */
#/* the items using the Python list sort feature.                            */
#/****************************************************************************/
def SortGetKey(Object):
   return Object.GetScheduleDate()


class Schedule:

   def __init__(self):
# Period between saving schedules to prevent exceesive saving.
      self.SavePeriod = datetime.timedelta(0, 300)
      self.SaveDateTime = datetime.datetime.now()
# Define an array to store the schedule items in.
      self.ScheduleItems = []


#/*************************************/
#/* Get the number of schedule items. */
#/*************************************/
   def GetItemCount(self):
      return len(self.ScheduleItems)


#/*********************************************/
#/* Get the item at the specific array index. */
#/*********************************************/
   def GetItem(self, ItemIndex):
      if len(self.ScheduleItems) > ItemIndex:
         return self.ScheduleItems[ItemIndex]
      else:
         return False


#/**************************************************/
#/* Find the schedule item with the specificed ID. */
#/**************************************************/
   def FindItem(self, FindItemID):
      ThisItem = False
      for ThisScheduleItem in self.ScheduleItems:
         if ThisScheduleItem.GetItemID() == FindItemID:
            ThisItem = ThisScheduleItem
      return ThisItem


#/*******************************************************/
#/* Function to display the current schedule of events. */
#/* In a tabulated form.                                */
#/*******************************************************/
   def DisplaySchedule(self, UserInterface, LineNumber, SelectedItemIndex, DisplayItemCount):
      Result = False
      for Count in range(0, DisplayItemCount):
         if SelectedItemIndex + Count < len(self.ScheduleItems):
            if Count == 0:
               Result = self.ScheduleItems[SelectedItemIndex + Count].GetItemID()
               SelectLeftChar = ">"
            else:
               SelectLeftChar = " "
            self.ScheduleItems[SelectedItemIndex + Count].DisplayItem(UserInterface, LineNumber + Count * 2, SelectLeftChar)
         else:
            UserInterface.PrintLine(LineNumber + Count * 2, "{: <20}".format(""))
            UserInterface.PrintLine(LineNumber + 1 +  Count * 2, "{: <20}".format(""))
      return Result


#/*************************************************/
#/* Add a new schedule item to the schedle array. */
#/*************************************************/
   def AddSchedule(self, NewRelayNumber, NewScheduleDate, NewRelayState, NewRepeat):
      self.ScheduleItems.append(ScheduleItem.ScheduleItem(NewRelayNumber, NewScheduleDate, NewRelayState, NewRepeat))
      self.SortSchedule()
      self.Save(True)


#/**************************************************/
#/* Delete a schedule item from the schedle array. */
#/**************************************************/
   def DelSchedule(self, ItemID):
      ThisScheduleItem = self.FindItem(ItemID)
      if ThisScheduleItem:
         self.ScheduleItems.remove(ThisScheduleItem)
      self.SortSchedule()
      self.Save(True)


#/*********************************************/
#/* Sort the list of schedule items so the    */
#/* expired items are at the top of the list. */
#/*********************************************/
   def SortSchedule(self):
      self.ScheduleItems.sort(key=SortGetKey)


#/*************************************************************************/
#/* If the top schedule item is in the past return it's ID as being       */
#/* triggered. The schedule items are kept in date order, so the top item */
#/* is the one which will trigger first. The calling function is          */
#/* responsible for removing the triggered item from the scheduled items  */
#/* or updating the scheduled item if the item is to be  repeated once    */
#/* the calling function has processed it; by calling the function:       */
#/* SetNextScheduleDate().                                                */
#/*************************************************************************/
   def ScheduleTrigger(self):
      ThisItemID = False
      Now = datetime.datetime.now()
      ThisItem = self.GetItem(0)
      if ThisItem and ThisItem.GetScheduleDate() <= Now:
         ThisItemID = ThisItem.GetItemID()
      return ThisItemID


#/*********************************************************************/
#/* Set the date and time of the specified schedule item to it's next */
#/* trigger date/time. If the item does not have a repeat period,     */
#/* remove the schedule item.                                         */
#/*********************************************************************/
   def SetNextScheduleDate(self, ThisItemID):
      ThisItem = self.FindItem(ThisItemID)
      if ThisItem and ThisItem.SetNextScheduleDate() == False:
         self.DelSchedule(ThisItemID)
      self.SortSchedule()
      self.Save(False)


#/************************************************************************/
#/* Save all schedule items to a file, so they can be reloaded when the  */
#/* application next starts and continue where the application left off. */
#/************************************************************************/
   def Save(self, Force):
      Now = datetime.datetime.now()
      if Force or Now > self.SaveDateTime + self.SavePeriod:
         File = open("Data/Schedule.txt", 'w', 0)
         for ThisScheduleItem in self.ScheduleItems:
            ThisScheduleItem.Save(File)
         File.close()
         self.SaveDateTime = Now


#/******************************************************/
#/* Load all of the schedule items from a file, so the */
#/* application can resume where it last left off.     */
#/******************************************************/
   def Load(self):
      try:
         File = open("Data/Schedule.txt", 'r', 0)
         Result = True
         while Result:
            NewSchedule = ScheduleItem.ScheduleItem(0, 0, 0, 0)
            Result = NewSchedule.Load(File)
            if Result:
               self.ScheduleItems.append(NewSchedule)
         File.close()
         self.SortSchedule()
      except:
         print("")

