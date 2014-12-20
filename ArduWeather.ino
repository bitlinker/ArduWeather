#include <TimerOne.h>
#include <Wire.h>
#include <OregonDecoder.h>
#include <dht.h>
#include <Adafruit_BMP085.h>

#include <SoftwareSerial.h>

#define LED 13 // LED on D13

#define OREGON_PIN 2  // D2 - using hardware level change interrupt
#define DHT22_PIN 5   // D5 - DHT22 thermo/humidity
// BMP085 is on A4 and A5 pins

#define LOCAL_SENSORS_UPDATE_TIMEOUT 10000000 // us

#define DEVICE_NAME "ArduWeather 1.0"

OregonDecoderV2 orscV2;
dht dhtReader;
Adafruit_BMP085 bmpReader;

volatile word pulse = 0;
volatile bool isLocalReportTimeout = false;

// Oregon receiver interrupt
void oregon_int(void)
{
  static word last = micros();
  pulse = micros() - last;
  last += pulse;
}

// Timer interrupt
void local_timeout_int(void)
{
  isLocalReportTimeout = true;
}

void printProtocolHeader() {
  Serial.print("{");
  
  // Device name and version
  Serial.print("\"device\":\"");
  Serial.print(DEVICE_NAME);
  Serial.print("\",");
  
  // Sensors array start
  Serial.print("\"sensors\":[");
}

void printProtocolFooter() {
  // Sensors array end and closing bracket
  Serial.println("]}");
}

void reportLocal()
{
  printProtocolHeader();
  
  // DHT22
  if (dhtReader.read22(DHT22_PIN) == DHTLIB_OK)
  {
    Serial.print("{\"DHT22\":{\"H\":");
    Serial.print(dhtReader.humidity);
    Serial.print(",\"T\":");
    Serial.print(dhtReader.temperature);
    Serial.print("}},");
  }
  
  // BMP085
  Serial.print("{\"BMP085\":{\"T\":");
  Serial.print(bmpReader.readTemperature());
  Serial.print(",\"P\":");
  Serial.print(bmpReader.readPressure());
  Serial.print("}}");
  
  printProtocolFooter();
}

void reportOregon ()
{
  printProtocolHeader();
  
  Serial.print("{\"oregon\":{\"data\":\"");
  byte pos;
  const byte* data = orscV2.getData(pos);
  for (byte i = 0; i < pos; ++i)
  {
    Serial.print(data[i] >> 4, HEX);
    Serial.print(data[i] & 0x0F, HEX);
  }
  Serial.print("\"}}");
  
  printProtocolFooter();
}

void setup () 
{
  Serial.begin(115200);

  // Oregon
  pinMode(OREGON_PIN, INPUT);
  digitalWrite(OREGON_PIN, HIGH);
  attachInterrupt(0, oregon_int, CHANGE);
  
  // LED
  pinMode(LED, OUTPUT);
  
  // BMP085
  if (!bmpReader.begin())
  {
    digitalWrite(LED, HIGH); // Error
    while (1) {}
  }
  
  // Local sensors update timer
  Timer1.initialize(LOCAL_SENSORS_UPDATE_TIMEOUT);
  Timer1.attachInterrupt(local_timeout_int);
}


void loop ()
{  
  noInterrupts();
  word p = pulse;
  pulse = 0;
  interrupts();

  if (isLocalReportTimeout)
  {
    digitalWrite(LED, HIGH);
    reportLocal();
    isLocalReportTimeout = false;
    digitalWrite(LED, LOW);
  }

  // Oregon sensors
  if (p != 0)
  {
    if (orscV2.nextPulse(p)) 
    {
      digitalWrite(LED, HIGH);
      reportOregon();
      orscV2.resetDecoder();
      digitalWrite(LED, LOW);
    }
  }  
}
