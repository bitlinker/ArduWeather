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
