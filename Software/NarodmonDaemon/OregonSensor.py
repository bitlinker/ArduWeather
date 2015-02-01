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

from Sensor import Sensor
from SensorValue import SensorValue

# Oregon weather station sensor class
class OregonSensor(Sensor):
    SENSOR_TYPE_THN132N = 'THN132N'
    SENSOR_TYPE_THGN132N = 'THGN132N'

    VALUE_BATTERY = 'B'

    __type = None
    __battery = None
    __id = None
    __channel = None

    def __init__(self, type, id, channel, batteryHigh):
        Sensor.__init__(self, type)
        self.__type = type
        self.__id = id
        self.__channel = channel
        self.__battery = batteryHigh

    def getType(self):
        return self.__type

    def getBatteryHigh(self):
        return self.__battery

    def getId(self):
        return self.__id

    def getChannel(self):
        return self.__channel

    def getUUID(self):
        return self.getName() + self.__id + str(self.__channel)

    def getValuesList(self):
        result = Sensor.getValuesList(self)

        if (self.__battery):
            result.append(SensorValue(self.getUUID(), self.VALUE_BATTERY, self.__battery))

        return result
