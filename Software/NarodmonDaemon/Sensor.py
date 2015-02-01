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

from SensorValue import SensorValue

class Sensor:
    VALUE_TEMPERATURE = 'T'
    VALUE_HUMIDITY = 'H'
    VALUE_PRESSURE = 'P'

    __name = None
    __temperature = None   # In Celsius degrees
    __humidity = None      # In percent
    __pressure = None      # In mmHg

    def __init__(self, name):
        self.__name = name

    def getName(self):
        return self.__name

    def getTemperature(self):
        return self.__temperature

    def getHumidity(self):
        return self.__humidity

    def getPressure(self):
        return self.__pressure

    def setTemperatureC(self, temp):
        self.__temperature = temp

    def setTemperatureF(self, temp):
        self.__temperature = (temp - 32) / 1.8

    def setHumidity(self, humidity):
        self.__humidity = humidity

    def setPressureMMHg(self, pressure):
        self.__pressure = pressure

    def setPressurePa(self, pressure):
        self.__pressure = pressure * 0.00750061683

    def getUUID(self):
        return self.getName()

    def getValuesList(self):
        result = []

        if (self.__temperature):
            result.append(SensorValue(self.getUUID(), self.VALUE_TEMPERATURE, self.__temperature))

        if (self.__humidity):
            result.append(SensorValue(self.getUUID(), self.VALUE_HUMIDITY, self.__humidity))

        if (self.__pressure):
            result.append(SensorValue(self.getUUID(), self.VALUE_PRESSURE, self.__pressure))

        return result
