#include <LiquidCrystal.h>
#define PIN_BL 10

LiquidCrystal lcd(8, 9, 4, 5, 6, 7);
String s = "";

void setup () {
  Serial.begin(9600);
  lcd.begin(16, 2);
  pinMode(PIN_BL, OUTPUT);
  analogWrite(PIN_BL, 100);
  
  char shake = '0';
  while (shake != 'R') {
    if (Serial.available()) {
      shake = Serial.read();
    }
  }
  
  Serial.println("S");
}

void loop () {
  while (Serial.available() > 0) {
    char r = Serial.read();
    
    if (r == '\n') {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(s);
      break;
    }
    
    s += r;
  }
  
  delay(50);
}
