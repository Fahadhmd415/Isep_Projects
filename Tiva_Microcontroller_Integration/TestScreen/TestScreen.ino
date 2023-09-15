
#include "Iseplogo128.h"
#define LED GREEN_LED

void setup() {
  // put your setup code here, to run once:
  int pin = 33;
  
pinMode(RED_LED, OUTPUT);  
pinMode(BLUE_LED, OUTPUT);
pinMode(GREEN_LED, OUTPUT);
pinMode(pin,OUTPUT);  

Serial.begin(9600);   
Serial1.begin(9600);
Serial1.print("AT+NAMEINTELI"); 

InitI2C();
InitScreen();

Display(motif);                           // affichage de l'image décrite dans le tabelau de donnée motif.h
//DisplayString(0,5,"APP ISEP");            // Ecriture sur la 5ème ligne 
DisplayString(30,7,"Live healthy");  // Ecriture sur la dernière ligne. 



// void test_fft(); // La fonction test_fft disponible dans le fichier fft.ino montre comment utiliser la fft

}

void loop() {
  //digitalWrite(RED_LED, HIGH);
  //digitalWrite(BLUE_LED, HIGH);
  digitalWrite(GREEN_LED, HIGH);
  digitalWrite(LED, HIGH); 
  
  
  delay(100);
  delay(100);
  int i;
  i = analogRead(28);
  Serial1.print("Value : "); Serial1.println(i);
  
  Serial.print("Value : ");  Serial.println(i);           // debug value
  delay(500);

  // put your main code here, to run repeatedly: 
   if (Serial1.available()) {
    int inByte = Serial.read();
    Serial1.write(inByte);
  }
    if (Serial1.available()) {
    int inByte = Serial.read();
    Serial1.write(inByte);
  }

}
