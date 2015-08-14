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
#/* PiTimer - Step 1 - Programatically setting the system time.              */
#/* ------------------------------------------------------------------------ */
#/* V1.00 - 2015-07-04 - Jason Birch                                         */
#/* ------------------------------------------------------------------------ */
#/* Initial code for a relay timer. This code simply demonstraes setting and */
#/* displaying the Raspberry Pi OS time using Python code.                   */
#/*                                                                          */
#/* The code requires permission in the OS to set the system time so needs   */
#/* to be run as the super user currently, using the following command in a  */
#/* terminal window:                                                         */
#/*                                                                          */
#/* sudo python PiTimer.py                                                   */
#/****************************************************************************/


import os
import datetime


#/***************************************************************/
#/* Function to display the system time in a consistant format. */
#/***************************************************************/
def PrintSystemTime():
   Now = datetime.datetime.now()
   print(Now.strftime("CURRENT SYSTEM TIME: %Y-%m-%d %H:%M:%S"))


#/*******************************************************************/
#/* Function to set the system time to the specified date and time. */
#/*******************************************************************/
def SetSystemTime(NewTime):
   os.system("date -s '" + NewTime + "' > /dev/null")


#/**************************************************************************/
#/* Main application procedure.                                            */
#/* Currently just a test procedure to demonstrate setting the system time */
#/* and date, and displaying it, several times.                            */
#/**************************************************************************/
SetSystemTime("2012-08-02 15:22:34")
PrintSystemTime()

SetSystemTime("1981-12-25 05:45:30")
PrintSystemTime()

SetSystemTime("2015-06-15 19:35:00")
PrintSystemTime()

