char data;
int ledPin = 13;

void setup () {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  
  // Send test data
  for (int i = 0; i < 5; i++) {
    Serial.println(i);
  }
  
  delay(1000);
}

void loop () {
//  Serial.println("test data");
  delay(1000);
//  Serial.println("test data 2");
  delay(1000);
  
  if (Serial.available()) {
    data = Serial.read();
    blinkLed();
  }
}

void blinkLed () {
  for (int i = 0; i < 2; i++) {
    digitalWrite(ledPin, HIGH);
    delay(500);
    digitalWrite(ledPin, LOW);
    delay(500);
  }
}
