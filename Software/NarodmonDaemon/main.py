# Copyright (c) 2015 bitlinker@gmail.com
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import logging
import datetime
from narodmon import Narodmon
from DeviceParser import DeviceParser
from DeviceReader import DeviceReader
from Config import Config

class ArduWeatherApp:

    __oldtime = None
    __sensorValues = {}

    def __init__(self):
        logging.basicConfig(level = Config.LOGGING_LEVEL)
        logging.info('ArduWeatherApp started')

        try:
            self.narodmonProtocol = Narodmon()
            self.deviceReader = DeviceReader(Config.COM_PORT, Config.COM_SPEED)
        except (serial.SerialException, IOError) as  e:
            logging.error('Error during initialization: ' + str(e))
            sys.exit()

    def run(self):
        logging.info('Entering mainloop')
        self.deviceReader.readLoop(self)

    # Callback called on new data reception form device
    def dataCallback(self, dataLine):
        try:
            deviceParser = DeviceParser(dataLine)
            name = deviceParser.getDeviceName();
            sensors = deviceParser.getSensors();
            for sensor in sensors:
                self.__updateSensorData(sensor)
        except ValueError, e:
            logging.error('Error processing data: ' + str(e))
            return False

        try:
            self.__sendSensorData()
        except ValueError, e:
            logging.error('Error sending data: ' + str(e))
            self.__sensorValues = {}
            return False

        return True

    def __updateSensorData(self, sensor):
        for value in sensor.getValuesList():
            valueName = value.getSensorUUID() + value.getName()
            self.__sensorValues[valueName] = value

    def __sendSensorData(self):
        curtime = datetime.datetime.now()

        if not self.__oldtime or (curtime - self.__oldtime > Config.SEND_INTERVAL):
            self.__oldtime = curtime

            if len(self.__sensorValues) > 0:
                res = self.narodmonProtocol.send(Config.DEVICE_MAC, Config.DEVICE_NAME, self.__sensorValues.values())

            self.__sensorValues = {}

# Entry point
if __name__ == "__main__":
    app = ArduWeatherApp()
    app.run()
