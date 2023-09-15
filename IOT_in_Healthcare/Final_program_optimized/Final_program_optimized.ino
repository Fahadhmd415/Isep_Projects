#include <Arduino_LSM6DS3.h>
#include <SoftwareSerial.h>
#include <TinyGPS++.h>
#include <LiquidCrystal.h>

#define RX_PIN 12
#define TX_PIN 13

SoftwareSerial ss(RX_PIN, TX_PIN);
TinyGPSPlus gps;

int steps = 0;
int fallThreshold = 2; // adjust this value to change the fall detection sensitivity
unsigned long fallTime;
bool fallDetected = false;
float lat;
float lng;
bool displayValue1 = true;

LiquidCrystal lcd(11, 2, 3, 5, 6, 7);

void setup() {
  lcd.begin(16, 2);
  Serial.begin(9600);
  ss.begin(9600);
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
}

void loop() {
  float xAcc, yAcc, zAcc, xGyr, yGyr, zGyr;

  while (ss.available() > 0) {
    if (gps.encode(ss.read())) {
      Serial.print("Longitude= ");
      Serial.println(gps.location.lng(), 2);
      Serial.print("Lattitude= ");
      Serial.println(gps.location.lat(), 2);
      delay(100);
    }
  }

  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
    IMU.readAcceleration(xAcc, yAcc, zAcc);
    float accMag = sqrtf(xAcc * xAcc + yAcc * yAcc + zAcc * zAcc);

    if (accMag > 1.10) {
      steps += 2;
      Serial.print("Step = ");
      Serial.println(steps);
      delay(100);
    }
   else {
      Serial.print("Step = ");
      Serial.println(steps);
      delay(100);
    }

    if (accMag > fallThreshold) {
      fallDetected = true;
      Serial.println("Fall = Potential fall detected");

      fallTime = millis();
      delay(3000); // delay 3 secs
      IMU.readAcceleration(xAcc, yAcc, zAcc);
      float accMag2 = sqrtf(xAcc * xAcc + yAcc * yAcc + zAcc * zAcc);
      if (accMag2 < 1.05) {
        Serial.println("Fall1 = Fall detected!");
        lcd.setCursor(0, 1);
        lcd.print("Fall detected");
        delay(600000);
        lcd.clear();
      } else {
        Serial.println("Fall2 = False positive!");
      }
      fallDetected = false;
    }
  }

  lcd.setCursor(0,0);
  lcd.print("Step = ");
  lcd.print(steps);
  delay(1000);
  lcd.clear();
}
