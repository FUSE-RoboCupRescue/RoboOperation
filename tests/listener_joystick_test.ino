// Teensy 4.1 Listener
const int LED_PIN = 13; // Use onboard LED for visual confirmation

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  while (!Serial); 
}

void loop() {
  if (Serial.available() > 0) {
    // Read the incoming string until newline
    String incoming = Serial.readStringUntil('\n');
    incoming.trim(); // Remove any whitespace

    if (incoming == "1") {
      // Action: Toggle LED
      digitalWrite(LED_PIN, HIGH);
      Serial.println("ACK: Button Command Received!");
      delay(100); 
      digitalWrite(LED_PIN, LOW);
    } else {
      Serial.print("ACK: Received Unknown: ");
      Serial.println(incoming);
    }
  }
}