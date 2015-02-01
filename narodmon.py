import socket
import logging
import pprint

pp = pprint.PrettyPrinter(indent=4)

# NarodMon protocol implementation
class Narodmon:
    SERVER_URL = 'narodmon.ru'
    SERVER_PORT = 8283

    def __init__(self):
        return

    def __send(self, formattedString):
        try:
            logging.info('Opening TCP connection on server: %s, port: %s', self.SERVER_URL, self.SERVER_PORT)
            sock = socket.socket()
            sock.connect((self.SERVER_URL, self.SERVER_PORT))
            sock.send(formattedString)
            data = sock.recv(1024)
            if str(data) != 'OK':
                raise ValueError('Invalid narodmon response: ' + str(data))
            sock.close()
        except socket.error, e:
            raise ValueError('TCP IO error: ' + str(e))

    def __formatSensorsString(self, deviceMac, deviceName, sensorValues):
        result = "#{}#{}\n".format(deviceMac, deviceName)
        for value in sensorValues:
            valueName = value.getSensorUUID() + value.getName()
            result = result + "#{}#{}\n".format(valueName, value.getValue())
        return result + "##";

    def send(self, deviceMac, deviceName, sensorValues):
        logging.info('Sending narodmon sensors data for device' + deviceName)
        logging.info(pp.pprint(sensorValues))
        formattedString = self.__formatSensorsString(deviceMac, deviceName, sensorValues)
        logging.debug(formattedString)
        return self.__send(formattedString)
