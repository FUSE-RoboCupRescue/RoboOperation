// Teensy 4.1 Listener Code
void setup() {
  Serial.begin(115200);
  while (!Serial) ; // Wait for Serial Monitor/USB to connect
}

void loop() {
  // 1. Send "Ready" signal until we get a response
  if (Serial.available() <= 0) {
    Serial.print('R'); 
    delay(1000); 
  } else {
    // 2. Read the incoming message
    String incoming = Serial.readStringUntil('\n');
    
    // 3. Send back an acknowledgment
    Serial.print("ACK: Received [");
    Serial.print(incoming);
    Serial.println("]");
  }
}