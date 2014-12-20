import socket, serial, sys, json, datetime, binascii

DEVICE_MAC = 'A603RN6Wweather'

SENSOR_ID_1 = DEVICE_MAC + '01'
SENSOR_ID_2 = DEVICE_MAC + '02'
SENSOR_ID_3 = DEVICE_MAC + '03'
SENSOR_ID_4 = DEVICE_MAC + '04'

SEND_INTERVAL = datetime.timedelta(minutes = 10)

# Returns channel or -1 if not found
def getOregonChannel(dataArray):
  return {
    0x10 : 1,
    0x20 : 2,
    0x40 : 3,
  }.get(dataArray[2], -1)

def getOregonBattery(dataArray):
  if dataArray[4] & 0x4:
    return "low"
  else:
    return "high"

def getOregonID(dataArray):
  return hex(dataArray[3])

def getOregonTemperature(dataArray):
  sign = 1
  if dataArray[6] & 0x8:
    sign = -1
  temp = ((dataArray[5] & 0xF0) >> 4) * 10 + (dataArray[5] & 0xF) + (((dataArray[4] & 0xF0) >> 4) / 10.0)
  return sign * temp

def getOregonHumidity(dataArray):
  return (dataArray[7] & 0xF) * 10 + ((dataArray[6] & 0xF0) >> 4)

def decodeOregon(data):
  result = {}
  
  binData = bytearray(binascii.unhexlify(data))
  if binData[0] == 0x1A and binData[1] == 0x2D:
    channel = getOregonChannel(binData)
    id = getOregonID(binData)
    battery = getOregonBattery(binData)
    temperature = getOregonTemperature(binData)
    humidity = getOregonHumidity(binData)
    print "Type: THGN132N"
    print "ID: ", id
    print "Channel: ", channel
    print "Battery: ", battery
    print "Temperature:", temperature
    print "Humidity:", humidity

  elif binData[0] == 0xEA and binData[1] == 0x4C:
    channel = getOregonChannel(binData)
    id = getOregonID(binData)
    battery = getOregonBattery(binData)
    temperature = getOregonTemperature(binData)
    print "Type: THN132N"
    print "ID: ", id
    print "Channel: ", channel
    print "Battery: ", battery
    print "Temperature:", temperature
    
  else:
    print "unknown sensor"

  return result


try:
  ser = serial.Serial('COM4', 115200)
except serial.SerialException, e:
  print("Can't open USB port")
  sys.exit()

oldtime = datetime.datetime.min

while True:
  json_str = ser.readline()
  try:
    data = json.loads(json_str)
    print "Received data: ", data
  except ValueError, e:
    print("JSON parsing exception")
    continue

  deviceName = data['device']
  print "Device: ", deviceName
  
  sensors = data['sensors']
  for sensor in sensors:
    sensorName = sensor.keys()[0]
    print "Sensor: ", sensorName
    
    if sensorName == 'BMP085':
      bmp085 = sensor[sensorName]
      print "T: ", bmp085['T']
      print "P: ", bmp085['P']
    elif sensorName == 'DHT22':
      dht22 = sensor[sensorName]
      print "T: ", dht22['T']
      print "H: ", dht22['H']
    elif sensorName == 'oregon':
      oregon = sensor[sensorName]
      decodeOregon(oregon['data'])
    else:
      print "Unknown sensor!"  

  # curtime = datetime.datetime.now()

  # if curtime - oldtime > SEND_INTERVAL:
    # oldtime = curtime
    # print("sending: ")
    # print curtime

    # try:
      # sock = socket.socket()
      # sock.connect(('narodmon.ru', 8283))
      # sock.send("#{}\n#{}#{}\n#{}#{}\n#{}#{}\n#{}#{}\n##".format(DEVICE_MAC, SENSOR_ID_1, data['temp1'], SENSOR_ID_2, data['temp2'], SENSOR_ID_3, data['press'], SENSOR_ID_4, data['hum']))
      # data = sock.recv(1024)
      # print data
      # sock.close()
    # except socket.error, e:
      # print('ERROR! Exception {}'.format(e))