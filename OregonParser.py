import binascii

from OregonSensor import OregonSensor

# Oregon data parser class
class OregonParser:
    def __init__(self):
        return

    def __getOregonChannel(self, dataArray):
        return {
            0x10 : 1,
            0x20 : 2,
            0x40 : 3,
        }.get(dataArray[2], None)

    def __getOregonBattery(self, dataArray):
        if dataArray[4] & 0x4:
            return 0
        else:
            return 1.5

    def __getOregonID(self, dataArray):
        return hex(dataArray[3])

    def __getOregonTemperature(self, dataArray):
        sign = 1
        if dataArray[6] & 0x8:
            sign = -1
        temp = ((dataArray[5] & 0xF0) >> 4) * 10 + (dataArray[5] & 0xF) + (((dataArray[4] & 0xF0) >> 4) / 10.0)
        return sign * temp

    def __getOregonHumidity(self, dataArray):
        return (dataArray[7] & 0xF) * 10 + ((dataArray[6] & 0xF0) >> 4)

    def parse(self, data):
        binData = bytearray(binascii.unhexlify(data))
        if binData[0] == 0x1A and binData[1] == 0x2D:
            sensor = OregonSensor(OregonSensor.SENSOR_TYPE_THGN132N, self.__getOregonID(binData), self.__getOregonChannel(binData), self.__getOregonBattery(binData))
            sensor.setTemperatureC(self.__getOregonTemperature(binData))
            sensor.setHumidity(self.__getOregonHumidity(binData))
            return sensor

        elif binData[0] == 0xEA and binData[1] == 0x4C:
            sensor = OregonSensor(OregonSensor.SENSOR_TYPE_THN132N, self.__getOregonID(binData), self.__getOregonChannel(binData), self.__getOregonBattery(binData))
            sensor.setTemperatureC(self.__getOregonTemperature(binData))
            return sensor

        else:
            raise ValueError('Unsupported Oregon sensor ' + str(data))
