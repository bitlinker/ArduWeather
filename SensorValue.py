
#Sensor value data
class SensorValue:

    def __init__(self, sensorUUID, name, value):
        self.__name = name
        self.__value = value
        self.__sensorUUID = sensorUUID

    def getSensorUUID(self):
        return self.__sensorUUID

    def getName(self):
        return self.__name

    def getValue(self):
        return self.__value

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '[SensorValue: UUID: ' + self.getSensorUUID() + ' name: ' + self.getName() + ' value: ' + str(self.getValue()) + ']'
