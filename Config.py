import logging
import datetime

# Configuration class
class Config:
    DEVICE_MAC = 'A603RN6Wweather'
    DEVICE_NAME = 'ArduWeather'

    COM_PORT = 'COM4'
    COM_SPEED = 115200
    
    LOGGING_LEVEL = logging.DEBUG
    
    SEND_INTERVAL = datetime.timedelta(minutes = 5)