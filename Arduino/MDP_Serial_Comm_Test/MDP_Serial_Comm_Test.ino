byte data;
int ledPin = 13;
char result[50];

void setup () {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  
  // Init
  startBlink();
  
  // Start serial
  Serial.println("START DATA SEND!");
  
  // Send number
  for (int i = 0; i < 10; i++) {
    Serial.println(i);
  }
}

void loop () {   
  // Wait
  delay(1000);
  
  // Read "TESTING"
  int i = 0;
  while (Serial.available()) {
    result[i++] = Serial.read();
  }
  
  char t[] = "TESTING";
  
  // Print data
  for (int j = 0; j < i; j++) {
    if (result[j] == t[j]) {
      startBlink();
      delay(1000);
    }
  }
}

void startBlink () {
  for (int i = 0; i < 4; i++) {
    digitalWrite(ledPin, HIGH);
    delay(100);
    digitalWrite(ledPin, LOW);
    delay(100);
  }
}
