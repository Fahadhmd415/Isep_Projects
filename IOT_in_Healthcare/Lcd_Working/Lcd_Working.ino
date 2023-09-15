#include <LiquidCrystal.h>

LiquidCrystal lcd(11,2,4,5,6,7);

void setup() {
  lcd.begin(16,2);

}

void loop()  {

  lcd.setCursor(1,0);
  lcd.print("Arduino Project");
  //delay(3000);
  lcd.setCursor(0,1);
  lcd.print("bla bla bla bla");
  delay(3000);
  lcd.clear();
 
  /*

  lcd.setCursor(2,1);
  lcd.print("Lcd Tutorial");
  delay(3000);

  lcd.clear();

  lcd.blink();
  delay(4000);
  lcd.setCursor(7,1);
  delay(3000);
  lcd.noBlink();
  */

}


