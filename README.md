# Heart Rate Monitor

### Short Description
This project is run from Main.py. There, as the Main is initialized, tkinter is initialized and prepared for display as well. From there, the heart of the Monitor is run: a while loop which loads data, finds the beats in the given data, finds the one and five minute averages, checks for alarms, keeps a ten minute log, and renders all the data to a tkinter display.

The Reader loads one multiplexed datum: one ECG data point and one PPG data point. This is done to work around the 12-bit data limitation: it can load 24 bits, which is exactly 3 bytes. Then the bytes can be split up, and then can be unpacked after they are padded with more 0 bits. The data points continue to be loaded and placed in an array until there are enough to satisfy the length of time for which the data needs to be loaded. The Reader passes the data it loads as arrays: one ECG array and one PPG array.

The data arrays are then passed to the BeatDetector, which finds beats by finding a threshold value. Then, whenever data jumps from below the threshold to above, it counts as a single beat. The BeatDetector passes the calculated instant heart rate from the given data length.

The instant heart rate is then passed to the HRProcessor. The processor adds the heart rates to queues of 1 minute, 5 minute, and 10 minutes length. The means of those queues are calculated and passed as the minute long averages for display. Any bradycardia or tachycardia is detected here as well. All is passed to the main for display. In case of alarm, a 10-minute log is written out to a text file that will be saved in the program's directory.

All data is then rendered in tkinter by updating StringVars.

### How to Use
Before running the Main, the user may change values in the __init__ method to change parameters of the file. The user may choose whether the file uses multiplexed 12- or 16-bit values, how much time of data to read in at a time, and how often to update the display. The last parameter is added to speed up the simulation of the Monitor--it does not have anything to do with how often the time or instant heart rate is updated.

When running from the Main, the console will prompt the user for a filename. Enter the desired file to be analyzed.

### Imported Packages
This program uses the following packages:
* `tkinter` to make display possible and to use StringVars
* `struct` to translate data from binary to usable integers
* `time` in order to use the sleep function so that the entire binary is not analyzed at once
* `queue` in order to use the queue structure for keeping track of 1, 5, and 10 minute heart rates
* `math` to use isnan() to protect against NaN values

### Limitations
The submitted heart rate monitor is functional--but not clean enough or robust enough:
* The program cannot handle inputs when the full loaded amount of data is NaN, only if some inserted values are NaN.
* The program is not tolerant of noise: if any noise happens around the threshold value, it will be counted as heart beats.

The file was designed one basically finished class at a time. This means that the end implementation is not as clean as it should be. For example, rather than having a whole class HRProcessor that took care of everything to do with instant heart rate, what it did should have been split into more classes, even perhaps subclasses of it. There should be no reason to be finding and signaling alarms in the same class as that which queues heart rates.
