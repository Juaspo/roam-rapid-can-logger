# roam-rapid-can-logger

Connect button switch to the GPIO pins as shown in the picture below

![gpio_pins](https://user-images.githubusercontent.com/20067958/196567847-fefdffec-0491-460a-b7cf-abc0ed7bfe57.png)

GPIO pins
green pins = RTC (pins 1-10), red pin (pin 35) = LED, yellow pin (pin 37) = Button, black pin (pin 39) = GND
![20221019_014953](https://user-images.githubusercontent.com/20067958/196567590-e8fa9499-6ca0-46b7-9848-916dc885955a.jpg)


Connect CAN wires to CAN0 can port and USB for power.
![20221019_021200](https://user-images.githubusercontent.com/20067958/196567495-6dd35f98-0c87-4bcb-ac62-8e52a46b73df.jpg)
Connect CAN data wires and USB for power.

Usage
Upon power the Raspberry pi will boot up which may take up to 30sec. After complete bootup sequence the script for CAN logging will automatically be initiated. If this is done successfully the LED light on the remote switch will flash rapidly 5 times. This indicates that the boot is complete, the script is running and that CAN data can start to be logged.

To start logging data, press the button once. The green LED will light up indicating that data is being logged.

To stop logging data just press the button again and the LED should turn off, indicating that that data collection has been stopped.

Note! During data logging, If no data is received within 2 seconds the logging sequence will stop to indicate that no further data is being received

CAN data is stored under /home/pi/canlogs/
