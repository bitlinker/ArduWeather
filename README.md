# ArduWeather
Yet another Arduino weather station project

This project is heading to create the portable device for measuring temperature, humidity and atmospheric pressure inside and outside the house and share that data using USB serial interface.

## Hardware
The hardware used:
* [Arduino](http://arduino.cc/en/Main/ArduinoBoardUno) compatible board (I used Arduino UNO)
* BMP085 pressure sensor with current-limiting resistors
* DHT22 temperature-humidity sensor
* 433 MHz Wireless Receiving Module for Oregon Scientific wireless sensors

The wiring is shown on the image below:
![Wiring](https://github.com/bitlinker/ArduWeather/blob/master/Images/wiring.png)

The DHT22 is powered by 5V and it's data out pin is connected to the Arduino D5 pin.
The BMP085 is powered by 3.3V, SDA is connected to A4 and SCL is connected to A5 - hardware I²C bus is used.
The receiver is powered by 5V and connected to D2 - hardware interrupt is used

The 17.3cm wire should be used for antenna on 433 Mhz. It's enough to get good signal from wireless sensor about 15m away blocked by 2 walls. The old modem casing was used. There are some photos of assembled device:
![Device internals](https://github.com/bitlinker/ArduWeather/blob/master/Images/internals.jpg)
![Assembled device](https://github.com/bitlinker/ArduWeather/blob/master/Images/device.jpg)

## Software
The Arduino firmware could be found in repository. The following libraries were used:
* [Adafruit_BMP085](https://github.com/adafruit/Adafruit-BMP085-Library)
* [DhtLib](http://playground.arduino.cc/Main/DHTLib)
* [TimerOne](http://playground.arduino.cc/Code/Timer1) - it was not really necessary, however really convenient.
* [ookDecoder](https://github.com/jimstudt/ook-decoder) - the version in repository was **patched** to work sucessfully with cheap chinese receivers which could pass initial bits from preamble.

NarodmonDaemon software is written in Python and used to read data from device and publish it to the [Public Monitoring](http://narodmon.ru/) project. It could be configured by Config.py file.
