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
#/* PiTimer - Step 3 - Schedule table.                                       */
#/* ------------------------------------------------------------------------ */
#/* V1.00 - 2015-07-04 - Jason Birch                                         */
#/* ------------------------------------------------------------------------ */
#/* Initial code for a relay timer. This code simply demonstraes setting and */
#/* displaying the Raspberry Pi OS time using Python code.                   */
#/*                                                                          */
#/* The code requires permission in the OS to set the system time so needs   */
#/* to be run as the super user currently using the following command in a   */
#/* terminal window:                                                         */
#/*                                                                          */
#/* sudo python PiTimer.py                                                   */
#/****************************************************************************/


import datetime
import SystemTime
import Schedule
import ScheduleItem


#/**************************************************************************/
#/* Main application procedure.                                            */
#/**************************************************************************/

# Instance of the system time class to handle system time and clock module.
ThisSystemTime = SystemTime.SystemTime()

# Instance of schedule class to store and process timer schedules.
ThisSchedule = Schedule.Schedule()


#   /*******************************************************************/
#  /* Get the time from the timer module, and set the system time to  */
# /* ensure the system time is correct at the start.                 */
#/*******************************************************************/
# BOOKMARK: THIS IS A PLACEHOLDER FOR WHEN THE CLOCK MODLUE IS IMPLEMENTED.
ThisSystemTime.SetSystemTime("2015-06-18 19:40:00")
print("CURRENT SYSTEM TIME: " + ThisSystemTime.SystemTimeString())

#  /***************************************************************************/
# /* Add some sample schedules to demonstrate displaying the schedule table. */
#/***************************************************************************/
# Example turn relay 1 on, on every minute and off every thirty seconds past the minute.
ThisSchedule.AddSchedule(1, datetime.datetime(2015, 6, 1, 0, 0, 0), ScheduleItem.RELAY_ON, datetime.timedelta(0, 60))
ThisSchedule.AddSchedule(1, datetime.datetime(2015, 6, 1, 0, 0, 30), ScheduleItem.RELAY_OFF, datetime.timedelta(0, 60))

# Example turn relay 2 on, on every 15 seconds past the minute and off every fourty five seconds past the minute.
ThisSchedule.AddSchedule(2, datetime.datetime(2015, 6, 1, 0, 0, 15), ScheduleItem.RELAY_ON, datetime.timedelta(0, 60))
ThisSchedule.AddSchedule(2, datetime.datetime(2015, 6, 1, 0, 0, 45), ScheduleItem.RELAY_OFF, datetime.timedelta(0, 60))

# Example toggle relay 3 every 15 seconds.
ThisSchedule.AddSchedule(3, datetime.datetime(2015, 6, 1, 0, 0, 00), ScheduleItem.RELAY_TOGGLE, datetime.timedelta(0, 15))

#  /***************************************/
# /* Display the current event schedule. */
#/***************************************/
ThisSchedule.DisplaySchedule(ThisSchedule.GetItem(2).GetItemID())

