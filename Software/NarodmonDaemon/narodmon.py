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
            logging.info('sent sucessfully')
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
