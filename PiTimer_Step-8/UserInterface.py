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
#/* PiTimer - Step 8 - Controlling physical relays.                          */
#/* ------------------------------------------------------------------------ */
#/* V1.00 - 2015-07-04 - Jason Birch                                         */
#/* ------------------------------------------------------------------------ */
#/* Class to handle user input, output display and interface state machine.  */
#/****************************************************************************/


import string
import operator
import datetime
import SystemTime
import Schedule
import ScheduleItem


# Constants to define current user interface display.
STATE_MAIN_MENU = 0
STATE_ADD_SCHEDULE = 1
STATE_DEL_SCHEDULE = 2
STATE_RELAY_STATES = 3
STATE_SCHEDULE = 4
STATE_SET_SYSTEM_TIME = 5
STATE_SHUTDOWN = 6

# Constants to define display modes.
MODE_STANDARD = 0
MODE_CONFIRM = 1


class UserInterface:

   def __init__(self, NewWIndow, NewThisSchedule, NewThisRelays):
# Store a reference to the system window class to display onto.
      self.ThisWindow = NewWIndow
# Store a reference to the schedule class to display schedule inforamtion.
      self.ThisSchedule = NewThisSchedule
# Store a reference to the relays class to display relay inforamtion.
      self.ThisRelays = NewThisRelays
# Create an instance of the system time class, to display the system time.
      self.ThisSystemTime = SystemTime.SystemTime()

# Display application splash screen on initialisation.
      self.DisplaySplash()

# Buffer for input strings.
      self.InputBuffer = ""
# List position, moved by user.
      self.SelectPos = 0
      self.SelectID = 0
# Display the initial user interface, the main menu.
      self.InterfaceState = STATE_MAIN_MENU


#/***************************************************/
#/* Display a splash screen for application startup */
#/* to show information about this application.     */
#/***************************************************/
   def DisplaySplash(self):
      self.ThisWindow.clear()
      self.ThisWindow.refresh()
      print("{:^20}".format("PiTimer") + "\r")
      print("{:^20}".format("2015-06-23") + "\r")
      print("{:^20}".format("Version 1.00") + "\r")
      print("{:^20}".format("(C) Jason Birch") + "\r")
      self.ThisWindow.refresh()


#/***********************************************************************/
#/* Distribute key press events to the current user interface function. */
#/***********************************************************************/
   def KeyPress(self, KeyCode):
      Result = KeyCode
      if self.InterfaceState == STATE_MAIN_MENU:
         Result = self.KeysMainMenu(KeyCode)
      elif self.InterfaceState == STATE_ADD_SCHEDULE:
         Result = self.KeysAddSchedule(KeyCode)
      elif self.InterfaceState == STATE_DEL_SCHEDULE:
         Result = self.KeysDelSchedule(KeyCode)
      elif self.InterfaceState == STATE_SCHEDULE:
         Result = self.KeysSchedule(KeyCode)
      elif self.InterfaceState == STATE_RELAY_STATES:
         Result = self.KeysRelayStates(KeyCode)
      elif self.InterfaceState == STATE_SET_SYSTEM_TIME:
         Result = self.KeysSetSystemTime(KeyCode)
      return Result


#/****************************************************************/
#/* Certain user interface displays need to update every second. */
#/****************************************************************/
   def DisplayRefresh(self):
      if self.InterfaceState == STATE_MAIN_MENU:
         self.DisplayMainMenu()
      elif self.InterfaceState == STATE_ADD_SCHEDULE:
         self.DisplayAddSchedule()
      elif self.InterfaceState == STATE_DEL_SCHEDULE:
         self.DisplayDelSchedule()
      elif self.InterfaceState == STATE_SCHEDULE:
         self.DisplaySchedule()
      elif self.InterfaceState == STATE_RELAY_STATES:
         self.DisplayRelayStates()
      elif self.InterfaceState == STATE_SET_SYSTEM_TIME:
         self.DisplaySetSystemTime()


#/*******************************************************/
#/* Change the current user interface to a new display. */
#/*******************************************************/
   def SetInterfaceState(self, NewInterfaceState):
# Start on standard display mode.
      self.Mode = MODE_STANDARD
# Clear the input buffer.
      self.InputBuffer = ""
# Reset list selection position.
      self.SelectPos =0
      self.SelectID = 0

      self.InterfaceState = NewInterfaceState

      if self.InterfaceState == STATE_MAIN_MENU:
         self.DisplayMainMenu()
      elif self.InterfaceState == STATE_ADD_SCHEDULE:
         self.DisplayAddSchedule()
      elif self.InterfaceState == STATE_DEL_SCHEDULE:
         self.DisplayDelSchedule()
      elif self.InterfaceState == STATE_SCHEDULE:
         self.DisplaySchedule()
      elif self.InterfaceState == STATE_RELAY_STATES:
         self.DisplayRelayStates()
      elif self.InterfaceState == STATE_SET_SYSTEM_TIME:
         self.DisplaySetSystemTime()


#/*********************************************************/
#/* Provided the input from the user and a mask to define */
#/* how to display the input, format a string to display. */
#/*********************************************************/
   def GetMaskedInput(self, Mask, Input):
      InputCount = 0
      Result = ""
      for Char in Mask:
         if Char == "#" and len(Input) > InputCount:
            Result += Input[InputCount:InputCount + 1]
            InputCount += 1
         else:
            Result += Char
      return Result


#/************************************************/
#/* Gather the input required for an input mask. */
#/************************************************/
   def KeyMaskedInput(self, Mask, Input, KeyCode):
# If a valid key is pressed, add to the input buffer.
      if len(Input) < Mask.count("#") and KeyCode >= ord("0") and KeyCode <= ord("9"):
         Input += chr(KeyCode)
# If delete key is pressed, delete the last entered key.
      elif KeyCode == 127 and len(Input) > 0:
         Input = Input[:-1]
      return Input


#/*****************************/
#/* MAIN MENU user interface. */
#/*****************************/
   def DisplayMainMenu(self):
      self.ThisWindow.clear()
      self.ThisWindow.refresh()
      print("{:>20}".format(self.ThisSystemTime.SystemTimeString()) + "\r")
      print("{:^20}".format("1 Add     4 Schedule") + "\r")
      print("{:^20}".format("2 Delete  5 Set Time") + "\r")
      print("{:^20}".format("3 Relays  6 Shutdown") + "\r")
      self.ThisWindow.refresh()


   def KeysMainMenu(self, KeyCode):
      Result = KeyCode
# If menu item 1 is selected, change to display add schedule.
      if KeyCode == ord("1"):
         self.SetInterfaceState(STATE_ADD_SCHEDULE)
# If menu item 2 is selected, change to display del schedule.
      if KeyCode == ord("2"):
         self.SetInterfaceState(STATE_DEL_SCHEDULE)
# If menu item 3 is selected, change to display relay states.
      if KeyCode == ord("3"):
         self.SetInterfaceState(STATE_RELAY_STATES)
# If menu item 4 is selected, change to display schedule.
      if KeyCode == ord("4"):
         self.SetInterfaceState(STATE_SCHEDULE)
# If menu item 5 is selected, change to display set system time.
      if KeyCode == ord("5"):
         self.SetInterfaceState(STATE_SET_SYSTEM_TIME)
# If menu item 6 is selected, return ESC key to the application main loop.
      if KeyCode == ord("6"):
         Result = 27
      return Result


#/********************************/
#/* RELAY STATES user interface. */
#/********************************/
   def DisplayRelayStates(self):
      self.ThisWindow.clear()
      self.ThisWindow.refresh()
      self.ThisRelays.DisplayRelayStates()
      self.ThisWindow.refresh()


   def KeysRelayStates(self, KeyCode):
      Result = KeyCode
# If enter key is pressed, change to display main menu.
      if KeyCode == 10:
         self.SetInterfaceState(STATE_MAIN_MENU)
      return Result


#/********************************/
#/* ADD SCHEDULE user interface. */
#/********************************/
   def DisplayAddSchedule(self):
      self.ThisWindow.clear()
      self.ThisWindow.refresh()
      print("{:^20}".format("ADD SCHEDULE") + "\r")
      print(self.GetMaskedInput("####-##-## ##:##:##\r\nPeriod ### ##:##:##\r\nRelay ##    State #\r", self.InputBuffer))
      self.ThisWindow.refresh()


   def KeysAddSchedule(self, KeyCode):
      Result = KeyCode
      self.InputBuffer = self.KeyMaskedInput("####-##-## ##:##:## ### ##:##:## ## #", self.InputBuffer, KeyCode)
# If enter key is pressed, change to display main menu.
      if KeyCode == 10:
# If full user input has been gathered, add a schedule item.
         if len(self.InputBuffer) == 26:
# Parse user input.
            UserInput = self.GetMaskedInput("####-##-## ##:##:## ### ##:##:## ## #", self.InputBuffer)
            RelayState = {
               "0":ScheduleItem.RELAY_OFF,
               "1":ScheduleItem.RELAY_ON,
               "2":ScheduleItem.RELAY_TOGGLE,
            }.get(UserInput[36:37], ScheduleItem.RELAY_TOGGLE)

            PeriodSeconds = string.atoi(UserInput[30:32]) + 60 * string.atoi(UserInput[27:29]) + 60 * 60 * string.atoi(UserInput[24:26]) + 24 * 60 * 60 * string.atoi(UserInput[20:23])
            PeriodDays = operator.div(PeriodSeconds, 24 * 60 * 60)
            PeriodSeconds = operator.mod(PeriodSeconds, 24 * 60 * 60)
# Add schedule item, ignore errors from invalid data entered.
            try:
               self.ThisSchedule.AddSchedule(string.atoi(UserInput[33:35]), datetime.datetime(string.atoi(UserInput[0:4]), string.atoi(UserInput[5:7]), string.atoi(UserInput[8:10]), string.atoi(UserInput[11:13]), string.atoi(UserInput[14:16]), string.atoi(UserInput[17:19])), RelayState, datetime.timedelta(PeriodDays, PeriodSeconds))
            except:
               print("")
            self.ThisWindow.refresh()

         self.SetInterfaceState(STATE_MAIN_MENU)
      return Result


#/********************************/
#/* DEL SCHEDULE user interface. */
#/********************************/
   def DisplayDelSchedule(self):
      self.ThisWindow.clear()
      self.ThisWindow.refresh()
      if self.Mode == MODE_STANDARD:
         print("{:^20}".format("DELETE SCHEDULE") + "\r")
         print("\r")
         if self.ThisSchedule.GetItemCount():
            self.SelectID = self.ThisSchedule.DisplaySchedule(self.SelectPos, 1)
         else:
            print("{:^20}".format("Empty") + "\r")
      elif self.Mode == MODE_CONFIRM:
         print("{:^20}".format("DELETE SCHEDULE") + "\r")
         print("\r")
         print("{:^20}".format("ARE YOU SURE?") + "\r")
         print("{:^20}".format("(4=N, 6=Y)") + "\r")
      self.ThisWindow.refresh()


   def KeysDelSchedule(self, KeyCode):
      Result = KeyCode
      if self.Mode == MODE_STANDARD:
# If a key at the top of the keypad is pressed, move up the list.
         if (KeyCode == ord("1") or KeyCode == ord("2") or KeyCode == ord("3")) and self.SelectPos > 0:
            self.SelectPos -= 1
# If a key at the bottom of the keypad is pressed, move down the list.
         elif (KeyCode == ord("0") or KeyCode == ord("7") or KeyCode == ord("8") or KeyCode == ord("9")) and self.SelectPos < self.ThisSchedule.GetItemCount() - 1:
            self.SelectPos += 1
# If enter key is pressed, enter confirm mode.
         if KeyCode == 10:
            if self.ThisSchedule.GetItemCount():
               self.Mode = MODE_CONFIRM
            else:
               self.SetInterfaceState(STATE_MAIN_MENU)
# If delete key is pressed, change to display main menu.
         if KeyCode == 127:
            self.SetInterfaceState(STATE_MAIN_MENU)
      elif self.Mode == MODE_CONFIRM:
         if KeyCode == ord("4"):
            self.SetInterfaceState(STATE_MAIN_MENU)
         elif KeyCode == ord("6"):
            self.ThisSchedule.DelSchedule(self.SelectID)
            self.SetInterfaceState(STATE_MAIN_MENU)

      return Result


#/************************************/
#/* CURRENT SCHEDULE user interface. */
#/************************************/
   def DisplaySchedule(self):
      self.ThisWindow.clear()
      self.ThisWindow.refresh()
      if self.ThisSchedule.GetItemCount():
         self.ThisSchedule.DisplaySchedule(self.SelectPos, 2)
      else:
         print("\r")
         print("{:^20}".format("Empty") + "\r")
      self.ThisWindow.refresh()


   def KeysSchedule(self, KeyCode):
      Result = KeyCode
# If a key at the top of the keypad is pressed, move up the list.
      if (KeyCode == ord("1") or KeyCode == ord("2") or KeyCode == ord("3")) and self.SelectPos > 0:
         self.SelectPos -= 1
# If a key at the bottom of the keypad is pressed, move down the list.
      elif (KeyCode == ord("0") or KeyCode == ord("7") or KeyCode == ord("8") or KeyCode == ord("9")) and self.SelectPos < self.ThisSchedule.GetItemCount() - 1:
         self.SelectPos += 1
# If enter key is pressed, change to display main menu.
      elif KeyCode == 10:
         self.SetInterfaceState(STATE_MAIN_MENU)
      return Result


#/***********************************/
#/* SET SYSTEM TIME user interface. */
#/***********************************/
   def DisplaySetSystemTime(self):
      self.ThisWindow.clear()
      self.ThisWindow.refresh()
      print("{:^20}".format("SET SYSTEM TIME") + "\r")
      print(self.GetMaskedInput("####-##-## ##:##:##\r", self.InputBuffer))
      self.ThisWindow.refresh()


   def KeysSetSystemTime(self, KeyCode):
      Result = KeyCode
      self.InputBuffer = self.KeyMaskedInput("####-##-## ##:##:##", self.InputBuffer, KeyCode)
# If enter key is pressed, change to display main menu.
      if KeyCode == 10:
# If full user input has been gathered, set the system time.
         if len(self.InputBuffer) == 14:
# BOOKMARK: THIS IS A PLACEHOLDER FOR WHEN THE CLOCK MODLUE IS IMPLEMENTED.
            self.ThisSystemTime.SetSystemTime(self.GetMaskedInput("####-##-## ##:##:##", self.InputBuffer))
         self.SetInterfaceState(STATE_MAIN_MENU)
      return Result

