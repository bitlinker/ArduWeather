#include <TimerOne.h>
#include <Wire.h>
#include <OregonDecoder.h>
#include <dht.h>
#include <Adafruit_BMP085.h>

#include <SoftwareSerial.h>

#define LED 13 // LED on D13

#define OREGON_PIN 2  // D2 - using hardware level change interrupt
#define DHT22_PIN 5  // D5 - DHT22 thermo/humidity

#define LOCAL_SENSORS_UPDATE_TIMEOUT 10000000 // us

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

void reportOregon (class DecodeOOK& decoder)
{
  byte pos;
  const byte* data = decoder.getData(pos);
  for (byte i = 0; i < pos; ++i)
  {
    Serial.print(data[i] >> 4, HEX);
    Serial.print(data[i] & 0x0F, HEX);
  }
  Serial.println();

  /*if(data[0] == 0x1A && data[1] == 0x2D)
  {
    Serial.print("[THGN132N,...] Id:");
    Serial.print(data[3], HEX);
    Serial.print(", Channel:");
    Serial.print(channel(data));
    Serial.print(", temp:");
    Serial.print(temperature(data));
    Serial.print(", hum:");
    Serial.print(humidity(data));
    Serial.print(", bat:");
    Serial.print(battery(data));
    Serial.println();
  }
  else if (data[0] == 0xEA && data[1] == 0x4C)
  {   
    Serial.print("[THN132N,...] Id:");
    Serial.print(data[3], HEX);
    Serial.print(", Channel:");
    Serial.print(channel(data));
    Serial.print(", temp:");
    Serial.print(temperature(data));
    Serial.print(", bat:");
    Serial.print(battery(data));
    Serial.println();
  }*/
}

void reportLocal()
{
  if (dhtReader.read22(DHT22_PIN) == DHTLIB_OK)
  {
    Serial.print("DHT Humidity = ");
    Serial.print(dhtReader.humidity);
    Serial.println(" %");
    
    Serial.print("DHT Temperature = ");
    Serial.print(dhtReader.temperature);
    Serial.println(" *C");
  }
  
  Serial.print("BMP Temperature = ");
  Serial.print(bmpReader.readTemperature());
  Serial.println(" *C");
  
  Serial.print("BMP Pressure = ");
  Serial.print(bmpReader.readPressure());
  Serial.println(" Pa");    
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
      reportOregon(orscV2);
      orscV2.resetDecoder();
      digitalWrite(LED, LOW);
    }
  }  
}

// TODO: decode on client side
/*float temperature(const byte* data)
{
  int sign = (data[6]&0x8) ? -1 : 1;
  float temp = ((data[5]&0xF0) >> 4)*10 + (data[5]&0xF) + (float)(((data[4]&0xF0) >> 4) / 10.0);
  return sign * temp;
}

byte humidity(const byte* data)
{
  return (data[7]&0xF) * 10 + ((data[6]&0xF0) >> 4);
}

// Ne retourne qu'un apercu de l'etat de la baterie : 10 = faible
byte battery(const byte* data)
{
  return (data[4] & 0x4) ? 10 : 90;
}

byte channel(const byte* data)
{
  byte channel;
  switch (data[2])
  {
  case 0x10:
    channel = 1;
    break;
  case 0x20:
    channel = 2;
    break;
  case 0x40:
    channel = 3;
    break;
  }
  return channel;
}*/

