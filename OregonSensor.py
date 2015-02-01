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
