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
#/* PiTimer - Step 2 - Python clesses.                                       */
#/* ------------------------------------------------------------------------ */
#/* V1.00 - 2015-07-04 - Jason Birch                                         */
#/* ------------------------------------------------------------------------ */
#/* This code demonstraes moving the code from step 1 into a simple class    */
#/* to demonstrate Python classes, befor moving onto larger Python classes.  */
#/*                                                                          */
#/* The code does the same as in step 1, sets and displays the system time   */
#/* several times in succession.                                             */
#/*                                                                          */
#/* The code requires permission in the OS to set the system time so needs   */
#/* to be run as the super user currently, using the following command in a  */
#/* terminal window:                                                         */
#/*                                                                          */
#/* sudo python PiTimer.py                                                   */
#/****************************************************************************/


import SystemTime


#/**************************************************************************/
#/* Main application procedure.                                            */
#/* Currently just a test procedure to demonstrate setting the system time */
#/* and date, and displaying it, several times.                            */
#/**************************************************************************/
ThisSystemTime = SystemTime.SystemTime()

ThisSystemTime.SetSystemTime("2012-08-02 15:22:34")
print("CURRENT SYSTEM TIME: " + ThisSystemTime.SystemTimeString())

ThisSystemTime.SetSystemTime("1981-12-25 05:45:30")
print("CURRENT SYSTEM TIME: " + ThisSystemTime.SystemTimeString())

ThisSystemTime.SetSystemTime("2015-06-15 19:35:00")
print("CURRENT SYSTEM TIME: " + ThisSystemTime.SystemTimeString())

