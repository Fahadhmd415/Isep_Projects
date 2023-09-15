
#include <SoftwareSerial.h>
#include <TinyGPS++.h>

#define RX_PIN 12
#define TX_PIN 13

SoftwareSerial ss(RX_PIN, TX_PIN);
TinyGPSPlus gps;

void setup() {
  Serial.begin(9600);
  ss.begin(9600);
}

void loop() {
  while (ss.available() > 0) {
    if (gps.encode(ss.read())) {
      Serial.print("Latitude= ");
      Serial.println(gps.location.lat(), 6);
      Serial.print("Longitude= ");
      Serial.println(gps.location.lng(), 6);
      delay(1000);
    }
  }
}