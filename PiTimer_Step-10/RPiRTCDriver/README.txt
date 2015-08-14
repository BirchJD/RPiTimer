RPi Real Time Clock
===================
Very low power battery backed clock to maintian the current time and date while
the Raspberry Pi is powered down.

The driver has been tested with Raspbian, Arch Linux and OpenElec XBMC.

The following files are distributed in the package:

README.txt            - Information about the package.
License.txt           - User license agreement.
License.dat           - License file.
RPiRTC                - Linux driver application.
RPiRTC.ini            - Driver configuration file.


Install
=======
For Linux distributions...
Copy the driver files into the directory:
/root/RPiRTCDriver/RPiRTC/

The software only has to run once when the system is booting. This can be done
as a cron job. To do this, at the command line type:
crontab -e

The system text editor will be used to edit the list of cron jobs. Add the
following line and then save the file:
@reboot /root/RPiRTCDriver/RPiRTC /S


When using with OpenElec XBMC...
Copy the driver files into the directory:
/storage/downloads/RPiRTCDriver/

The software only has to run once when the system is booting. To do this, edit
the file:
/storage/.config/autostart.sh
Add the following line and then save the file:
/storage/downloads/RPiRTCDriver/RPiRTC /S

OpenElec XBMC at the time of writing sets the date and time minus one hour for
some reason, which does't occur on Arch Linux or Raspbian. So when using
OpenElec XBMC, set the time on the device plus one hour to work around this.

