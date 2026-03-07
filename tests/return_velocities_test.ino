void setup() {
    Serial.begin(115200);
    while (!Serial);
}

void loop() {
    if (Serial.available() > 0) {
        String incoming = Serial.readStringUntil('\n');
        incoming.trim();

        float velocity[6];
        int count = 0;
        String temp = incoming;

        while (temp.length() > 0 && count < 6) {
            int idx = temp.indexOf(' ');
            String token = (idx == -1) ? temp : temp.substring(0, idx);
            velocity[count++] = token.toFloat();
            if (idx == -1) break;
            temp = temp.substring(idx + 1);
        }

        for (int i = 0; i < count; i++) {
            Serial.print("velocity ");
            Serial.print(i + 1);
            Serial.print(": ");
            Serial.print(velocity[i], 4);
            Serial.print("\r\n");  // explicit carriage return + newline
        }
    }
}