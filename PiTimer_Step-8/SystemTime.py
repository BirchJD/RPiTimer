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
#/* Class to handle system time procedures such as setting and reading the   */
#/* system time and setting and reading the clock module time.               */
#/****************************************************************************/


import os
import datetime


class SystemTime:

#/**************************************************************/
#/* Function to return the system time in a consistant format. */
#/**************************************************************/
   def SystemTimeString(self):
      Now = datetime.datetime.now()
      return Now.strftime("%Y-%m-%d %H:%M:%S")


#/*******************************************************************/
#/* Function to set the system time to the specified date and time. */
#/*******************************************************************/
   def SetSystemTime(self, NewTime):
	   os.system("date -s '" + NewTime + "' > /dev/null")

