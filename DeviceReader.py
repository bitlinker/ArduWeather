import logging
import serial

#ArduWeather serial port protocol reader
class DeviceReader:
    def __init__(self, portName, portSpeed):
        self.port = serial.Serial(portName, portSpeed)

    def readLoop(self, callback):
        while True:
            line = self.port.readline()
            logging.debug('New device data: ' + line)
            if callback != None:
                callback.dataCallback(line)
