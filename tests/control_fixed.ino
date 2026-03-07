#define ML_FB 20
#define ML_BRK 19
#define ML_SPD 33

#define MR_FB 39
#define MR_BRK 37
#define MR_SPD 15

#define F1_FB 12
#define F1_BRK 24
#define F1_SPD 3

#define F2_FB 9
#define F2_BRK 10
#define F2_SPD 2

#define F3_FB 30
#define F3_BRK 31
#define F3_SPD 4

#define F4_FB 40
#define F4_BRK 41
#define F4_SPD 14


void setup() {
    Serial.begin(115200);
    while (!Serial);

    // motor l
    pinMode(ML_FB, OUTPUT); //FB
    pinMode(ML_BRK, OUTPUT); //break
    analogWriteFrequency(ML_SPD, 1000);

    // motor r
    pinMode(MR_FB, OUTPUT);
    pinMode(MR_BRK, OUTPUT);
    analogWriteFrequency(MR_SPD, 1000);

    // flipper 1
    pinMode(F1_FB, OUTPUT);
    pinMode(F1_BRK, OUTPUT);
    analogWriteFrequency(F1_FB, 1000);

    // flipper 2
    pinMode(F2_FB, OUTPUT);
    pinMode(F2_BRK, OUTPUT);
    analogWriteFrequency(F2_FB, 1000);

    // flipper 3
    pinMode(F3_FB, OUTPUT);
    pinMode(F3_BRK, OUTPUT);
    analogWriteFrequency(F3_FB, 1000);

    // flipper 4
    pinMode(F4_FB, OUTPUT);
    pinMode(F4_BRK, OUTPUT);
    analogWriteFrequency(F4_FB, 1000);

    driveMR(0);
    driveML(0);
    driveF1(0);
    driveF2(0);
    driveF3(0);
    driveF4(0);
}

void loop() {
    if (Serial.available() > 0) {
        String incoming = Serial.readStringUntil('\n');
        incoming.trim();

        int velocity[6];
        int count = 0;
        String temp = incoming;

        while (temp.length() > 0 && count < 6) {
            int idx = temp.indexOf(' ');
            String token = (idx == -1) ? temp : temp.substring(0, idx);
            velocity[count++] = token.toInt();
            if (idx == -1) break;
            temp = temp.substring(idx + 1);
        }

        driveMR(velocity[0]);
        driveML(velocity[1]);
        driveF1(velocity[4]);
        driveF2(velocity[2]);
        driveF3(velocity[3]);
        driveF4(velocity[5]);

        for (int i = 0; i < count; i++) {
            Serial.print("velocity ");
            Serial.print(i + 1);
            Serial.print(": ");
            Serial.print(velocity[i]);;
            Serial.print(";");  // explicit carriage return + newline
        }
    }
}

void driveML(int spd) {
  if (spd > 0) {
    analogWrite(ML_SPD, 255 - spd); // needs to be remap to 255-0 (255 is stop 0 is max)
    digitalWrite(ML_BRK, 0);
    digitalWrite(ML_FB, 0);
  } else if (spd < 0) {
    analogWrite(ML_SPD, 255 + spd);
    digitalWrite(ML_BRK, 0);
    digitalWrite(ML_FB, 1);
  } else {
    analogWrite(ML_SPD, 255);
    digitalWrite(ML_BRK, 1);
    digitalWrite(ML_FB, 0);
  }
}

void driveMR(int spd) {
  if (spd > 0) {
    analogWrite(MR_SPD, 255 - spd);
    digitalWrite(MR_BRK, 0);
    digitalWrite(MR_FB, 0);
  } else if (spd < 0) {
    analogWrite(MR_SPD, 255 + spd);
    digitalWrite(MR_BRK, 0);
    digitalWrite(MR_FB, 1);
  } else {
    analogWrite(MR_SPD, 255);
    digitalWrite(MR_BRK, 1);
    digitalWrite(MR_FB, 0);
  }
}

void driveF1(int spd) {
  if (spd > 0) {
    analogWrite(F1_SPD, 255 - spd);
    digitalWrite(F1_BRK, 0);
    digitalWrite(F1_FB, 0);
  } else if (spd < 0) {
    analogWrite(F1_SPD, 255 + spd);
    digitalWrite(F1_BRK, 0);
    digitalWrite(F1_FB, 1);
  } else {
    analogWrite(F1_SPD, 255);
    digitalWrite(F1_BRK, 1);
    digitalWrite(F1_FB, 0);
  }
}

void driveF2(int spd) {
  if (spd > 0) {
    analogWrite(F2_SPD, 255 - spd);
    digitalWrite(F2_BRK, 0);
    digitalWrite(F2_FB, 0);
  } else if (spd < 0) {
    analogWrite(F2_SPD, 255 + spd);
    digitalWrite(F2_BRK, 0);
    digitalWrite(F2_FB, 1);
  } else {
    analogWrite(F2_SPD, 255);
    digitalWrite(F2_BRK, 1);
    digitalWrite(F2_FB, 0);
  }
}

void driveF3(int spd) {
  if (spd > 0) {
    analogWrite(F3_SPD, 255 - spd);
    digitalWrite(F3_BRK, 0);
    digitalWrite(F3_FB, 0);
  } else if (spd < 0) {
    analogWrite(F3_SPD, 255 + spd);
    digitalWrite(F3_BRK, 0);
    digitalWrite(F3_FB, 1);
  } else {
    analogWrite(F3_SPD, 255);
    digitalWrite(F3_BRK, 1);
    digitalWrite(F3_FB, 0);
  }
}

void driveF4(int spd) {
  if (spd > 0) {
    analogWrite(F4_SPD, 255 - spd);
    digitalWrite(F4_BRK, 0);
    digitalWrite(F4_FB, 0);
  } else if (spd < 0) {
    analogWrite(F4_SPD, 255 + spd);
    digitalWrite(F4_BRK, 0);
    digitalWrite(F4_FB, 1);
  } else {
    analogWrite(F4_SPD, 255);
    digitalWrite(F4_BRK, 1);
    digitalWrite(F4_FB, 0);
  }
}
