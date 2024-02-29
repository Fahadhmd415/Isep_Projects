#include <WiFiNINA.h>
#include <PubSubClient.h>

char ssid[] = "Redmi";
char pass[] = "87654321";
char mqtt_server[] = "192.168.180.153"; // Replace with your Raspberry Pi's IP address
char mqtt_topic1[] = "ecgData"; // New topic 1
char mqtt_topic2[] = "ecgData2"; // New topic 2

WiFiClient wifiClient;
PubSubClient client(wifiClient);

void setup() {
  Serial.begin(9600);
  pinMode(10, INPUT); // Setup for leads off detection LO +
  pinMode(11, INPUT); // Setup for leads off detection LO -
  setupWiFi();
}

void setupWiFi() {
  delay(10);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    if (WiFi.begin(ssid, pass) == WL_CONNECTED) {
      Serial.println("Connected to WiFi");
      delay(5000);
      client.setServer(mqtt_server, 1883);
      reconnect();
    } else {
      Serial.println("Connection failed. Retrying...");
      delay(5000);
    }
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.println("Attempting MQTT connection...");
    if (client.connect("ArduinoClient")) {
      Serial.println("connected to MQTT");
      delay(5000);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {
  static unsigned long previousMillis = 0;
  const unsigned long interval = 1000; // Interval in milliseconds (1 second)
  unsigned long currentMillis = millis();

  if ((digitalRead(10) == 1) || (digitalRead(11) == 1)) {
    Serial.println('!');
  } else {
    int sensorValue = analogRead(A0);
    float voltage = sensorValue * (3.3 / 1023.0); // Convert to millivolts
    Serial.println(voltage);

    if (client.connected()) {
      // Publish to the first topic
      client.publish(mqtt_topic1, String(voltage).c_str());
      // Publish to the second topic
      client.publish(mqtt_topic2, String(voltage).c_str()); // Modify data as needed
    } else {
      reconnect(); // Reconnect to MQTT broker if connection is lost
    }

    // Print the time in seconds on x-axis:
    if (currentMillis - previousMillis >= interval) {
      Serial.print("Time: ");
      Serial.print(currentMillis / 1000.0); // Convert milliseconds to seconds
      Serial.print("s, Voltage: ");
      Serial.print(voltage);
      Serial.println("V");
      previousMillis = currentMillis;
    }
  }

  // Wait for a bit to keep serial data from saturating
  delay(20);
}
