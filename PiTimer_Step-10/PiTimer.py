#!/usr/bin/python

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
#/* Add a class to read from a numeric keypad connected to the GPIO pins.    */
#/* Use the numeric keypad as an additional input to a keyboard.             */
#/*                                                                          */
#/* The code requires permission in the OS to set the system time so needs   */
#/* to be run as the super user currently using the following command in a   */
#/* terminal window:                                                         */
#/*                                                                          */
#/* sudo python PiTimer.py                                                   */
#/****************************************************************************/


import time
import datetime
import curses
import SystemTime
import Schedule
import ScheduleItem
import Relays
import Keypad
import UserInterface


#/**************************/
#/* Application constants. */
#/**************************/
GPIO_PINS = [ 5, 6, 12, 13, 14, 15, 16, 18, 19, 20, 21, 23, 24, 25, 26, 0, 0, 0, 0, 0 ]
GPIO_KEYPAD_PINS = [ 11, 7, 8, 9, 10, 22, 27 ]
MAX_RELAYS = 20
KEY_ESC = 27
MAIN_LOOP_PERIOD = 100
CHECK_SCHEDULE_COUNT = 10


#/**************************************************************************/
#/* Main application procedure.                                            */
#/**************************************************************************/
# Instance of the system time class to handle system time and clock module.
ThisSystemTime = SystemTime.SystemTime()
# Instance of schedule class to store and process timer schedules.
ThisSchedule = Schedule.Schedule()
# Instnace of relays class to store current relay states.
ThisRelays = Relays.Relays()
#Instance of keypad class to read key presses ona GPIO keypad.
ThisKeypad = Keypad.Keypad(GPIO_KEYPAD_PINS)

#  /*********************************************************/
# /* Configure the console so key presses can be captured. */
#/*********************************************************/
curses.initscr()
curses.noecho()
window = curses.newwin(80, 25)
window.nodelay(1)
window.timeout(0)

# Instance of user interface class to manage user interactions.
ThisUserInterface = UserInterface.UserInterface(window, ThisSchedule, ThisRelays)
time.sleep(1)

#   /*******************************************************************/
#  /* Get the time from the timer module, and set the system time to  */
# /* ensure the system time is correct at the start.                 */
#/*******************************************************************/
ModuleTime = ThisSystemTime.GetModuleTime()
ThisSystemTime.SetSystemTime(ModuleTime)

#    /*********************************************************/
#   /* Create an initial state for each realy in the system. */
#  /* Adding an extra item, as item 0 will be ignored so    */
# /* relay numbers start at a more user freindly 1.        */
#/*********************************************************/
for Count in range(MAX_RELAYS):
   if len(GPIO_PINS) > Count and GPIO_PINS[Count]:
      ThisRelays.AddRelay(Count + 1, Relays.RELAY_OFF, GPIO_PINS[Count])

#  /*********************************************************/
# /* Load schedule items from previous run of application. */
#/*********************************************************/
ThisSchedule.Load()

#   /********************************************/
#  /* Main application loop, this continues    */
# /* forever or until the ESC key is pressed. */
#/********************************************/
CheckScheduleCount = CHECK_SCHEDULE_COUNT
ExitFlag = False
while ExitFlag == False:

#  /*************************/
# /* Get a user key press. */
#/*************************/
   ThisKey = window.getch()

#   /*************************************************/
#  /* If a keyboard key has not been pressed, check */
# /* for a key press on the GPIO numeric keypad.   */
#/*************************************************/
   if ThisKey == -1:
      ThisKeypad.ScanKeypad()
      ThisKey = ThisKeypad.GetKeyCode()

#  /******************************************************/
# /* Pass user key presses to the user interface class. */
#/******************************************************/
   if ThisKey != -1:
      ThisKey = ThisUserInterface.KeyPress(ThisKey)

#  /**********************************************************/
# /* If the ESC key has been pressed, exit the application. */
#/**********************************************************/
   if ThisKey == KEY_ESC:
      ExitFlag = True

#  /**********************************************/
# /* Process main application loop every 250ms. */
#/**********************************************/
   curses.napms(MAIN_LOOP_PERIOD)

#  /********************************************/
# /* Process the schedule loop once a second. */
#/********************************************/
   CheckScheduleCount -= 1
   if CheckScheduleCount <= 0:
      CheckScheduleCount = CHECK_SCHEDULE_COUNT

#  /********************************************/
# /* Process all events which have triggered. */
#/********************************************/
      ThisItemID = True
      while ThisItemID:
#     /**************************************************************/
#    /* Check for a scheduled item which has moved into the past.  */
#   /* If an item is found process it and then remove it from the */
#  /* schedule. The item will automatically be rescheduled if    */
# /* required.                                                  */
#/**************************************************************/
         ThisItemID = ThisSchedule.ScheduleTrigger()
         if ThisItemID:
            ThisScheduleItem = ThisSchedule.FindItem(ThisItemID)
            ThisRelayAction = ThisScheduleItem.GetRelayState()
            ThisRelayNumber = ThisScheduleItem.GetRelayNumber()
            if ThisRelayAction == ScheduleItem.RELAY_OFF:
               ThisRelays.SetRelayState(ThisRelayNumber, Relays.RELAY_OFF)
            elif ThisRelayAction == ScheduleItem.RELAY_ON:
               ThisRelays.SetRelayState(ThisRelayNumber, Relays.RELAY_ON)
            else:
               ThisRelays.ToggleRelayState(ThisRelayNumber)
            ThisSchedule.SetNextScheduleDate(ThisItemID)

#  /****************************************************************/
# /* Certain user interface displays need to update every second. */
#/****************************************************************/
      ThisUserInterface.DisplayRefresh()

#  /*****************************************/
# /* Save application state before ending. */
#/*****************************************/
ThisSchedule.Save(True)

#  /*********************/
# /* Exit application. */
#/*********************/
curses.endwin()

#  /*********************************************/
# /* Close Raspberry Pi GPIO before finishing. */
#/*********************************************/
ThisRelays.CloseGPIO()

