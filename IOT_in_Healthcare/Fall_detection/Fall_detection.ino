#include <Arduino_LSM6DS3.h>

bool isFalling = false;

void setup() {
  Serial.begin(9600);
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
}

void loop() {
  float x, y, z;
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
    /*
    Serial.println(x);
    Serial.println(y);
    Serial.println(z);
    delay(1000);
    */
    if (z > -1.6 && !isFalling) { // Detect when user falls
      isFalling = true;

      Serial.println("Are you okay? You fell down!");
    } else if (z < -1.6 && isFalling) {
      isFalling = false;
      //Serial.println(x);
    }
    
  }
}