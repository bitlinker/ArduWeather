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

import json
from Sensor import Sensor
from OregonParser import OregonParser

#ArduWeather device protocol parser
class DeviceParser:

    SENSOR_BMP085 = 'BMP085'
    SENSOR_DHT22 = 'DHT22'
    SENSOR_OREGON = 'oregon'

    def __init__(self, dataLine):
        data = self.__parseJson(dataLine)

        self.__deviceName = data['device']
        self.__sensors = []

        sensorsJson = data['sensors']
        for sensorJson in sensorsJson:
            sensor = self.__parseSensor(sensorJson)
            self.__sensors.append(sensor)

    def __parseJson(self, dataLine):
        try:
            return json.loads(dataLine)
        except ValueError, e:
            raise ValueError('Cant parse json data: ' + str(e))

    def __parseSensor(self, sensorJson):
        name = sensorJson.keys()[0]
        sensorData = sensorJson[name]

        if name == self.SENSOR_BMP085:
            sensor = Sensor(name)
            sensor.setTemperatureC(sensorData['T'])
            sensor.setPressurePa(sensorData['P'])
            return sensor

        elif name == self.SENSOR_DHT22:
            sensor = Sensor(name)
            sensor.setTemperatureC(sensorData['T'])
            sensor.setHumidity(sensorData['H'])
            return sensor

        elif name == self.SENSOR_OREGON:
            oregonParser = OregonParser()
            sensor = oregonParser.parse(sensorData['data'])
            return sensor
        else:
            raise ValueError('Unknown sensor: ' + name)

    def getDeviceName(self):
        return self.__deviceName

    def getSensors(self):
        return self.__sensors
