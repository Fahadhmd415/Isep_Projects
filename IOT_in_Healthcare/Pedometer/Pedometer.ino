#include <Arduino_LSM6DS3.h>

int steps = 0;

void setup() {
  Serial.begin(9600);
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
}

void loop() {
 // Serial.print("hello");
  float x, y, z;
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
    //Serial.print(x);
    if (x > 1 || x < -1) {
      steps++;
      Serial.println(steps);
      delay(1000);
    }
  }
}

