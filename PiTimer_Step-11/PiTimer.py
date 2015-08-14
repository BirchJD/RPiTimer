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
#/* PiTimer - Step 11 - 20 x 4 LCD display.                                  */
#/* ------------------------------------------------------------------------ */
#/* V1.00 - 2015-07-04 - Jason Birch                                         */
#/* ------------------------------------------------------------------------ */
#/* Add a class to write to a 20 x 4 character LCD connected to the GPIO     */
#/* pins. Use the LCD as an additional display to a terminal.                */
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
import RPi.GPIO
import SystemTime
import Schedule
import ScheduleItem
import Relays
import Keypad
import LCD
import UserInterface


#/**************************/
#/* Application constants. */
#/**************************/
GPIO_PINS = [ 5, 6, 12, 13, 14, 15, 16, 18, 19, 20, 21, 23, 24, 25, 26, 0, 0, 0, 0, 0 ]
GPIO_KEYPAD_PINS = [ 11, 7, 8, 9, 10, 22, 27 ]
GPIO_LCD_PINS = [ 4, 17, 27, 22, 10, 9 ]
GPIO_LED_PINS = [ 4, 17 ]
LED_RED = 0
LED_GREEN = 1
MAX_RELAYS = 20
KEY_ESC = 27

TERMINAL = False
MAIN_LOOP_PERIOD = 0.1
CHECK_SCHEDULE_COUNT = 10
MAIN_LOOP_PERIOD_LCD = 0.001
CHECK_SCHEDULE_COUNT_LCD = 1000


#/**************************************************************************/
#/* Main application procedure.                                            */
#/**************************************************************************/
# Instance of the system time class to handle system time and clock module.
ThisSystemTime = SystemTime.SystemTime()
# Instance of schedule class to store and process timer schedules.
ThisSchedule = Schedule.Schedule()
# Instnace of relays class to store current relay states.
ThisRelays = Relays.Relays()
#Instance of keypad class to read key presses on a GPIO keypad.
ThisKeypad = Keypad.Keypad(GPIO_KEYPAD_PINS)
#Instance of LCD class to write to a GPIO LCD module.
ThisLCD = LCD.LCD(GPIO_LCD_PINS)

#  /*********************************************************/
# /* Configure the console so key presses can be captured. */
#/*********************************************************/
window = False
if TERMINAL:
   curses.initscr()
   curses.noecho()
   window = curses.newwin(80, 25)
   window.nodelay(1)
   window.timeout(0)

# Instance of user interface class to manage user interactions.
ThisUserInterface = UserInterface.UserInterface(window, ThisLCD, ThisSchedule, ThisRelays)

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

#  /*******************************************************/
# /* Write from LCD cache onto LCD at a manageable rate. */
#/*******************************************************/
   ThisLCD.WriteNibble()

   if ThisLCD.IsBusy() == False:
#  /*************************/
# /* Get a user key press. */
#/*************************/
      ThisKey = -1
      if TERMINAL:
         ThisKey = window.getch()

#   /*************************************************/
#  /* If a keyboard key has not been pressed, check */
# /* for a key press on the GPIO numeric keypad.   */
#/*************************************************/
      if ThisKey == -1:
         ThisKeypad.ScanKeypad()
         ThisKey = ThisKeypad.GetKeyCode()
#   /*************************************************************/
#  /* Set the red LED indicator off and green LED indicator on. */
# /* Indicators share GPIO pins with LCD and Keypad.           */
#/*************************************************************/
         RPi.GPIO.output(GPIO_LED_PINS[LED_RED], 1)
         RPi.GPIO.output(GPIO_LED_PINS[LED_GREEN], 0)

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

#  /***********************************************/
# /* Process main application loop every period. */
#/***********************************************/
      time.sleep(MAIN_LOOP_PERIOD)
      if CheckScheduleCount > CHECK_SCHEDULE_COUNT:
         CheckScheduleCount = CHECK_SCHEDULE_COUNT
   else:
#  /*********************************************************************/
# /* Process main application loop faster when data is queued for LCD. */
#/*********************************************************************/
      time.sleep(MAIN_LOOP_PERIOD_LCD)
      if CheckScheduleCount > CHECK_SCHEDULE_COUNT_LCD:
         CheckScheduleCount = CHECK_SCHEDULE_COUNT_LCD

#  /********************************************/
# /* Process the schedule loop once a second. */
#/********************************************/
   CheckScheduleCount -= 1
   if CheckScheduleCount <= 0:
      if ThisLCD.IsBusy() == False:
         CheckScheduleCount = CHECK_SCHEDULE_COUNT
      else:
         CheckScheduleCount = CHECK_SCHEDULE_COUNT_LCD

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
ThisLCD.Clear()
while ThisLCD.IsBusy():
   ThisLCD.WriteNibble()
   time.sleep(MAIN_LOOP_PERIOD_LCD)

if TERMINAL:
   curses.endwin()

#  /*********************************************/
# /* Close Raspberry Pi GPIO before finishing. */
#/*********************************************/
ThisRelays.CloseGPIO()

