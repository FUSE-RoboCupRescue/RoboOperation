// Tracks Right
#define MR_FB 39
#define MR_BRK 37
#define MR_SPD 15

// Tracks Left
#define ML_FB 20
#define ML_BRK 19
#define ML_SPD 33

// Flipper Front Right
#define FFR_FB 9
#define FFR_BRK 10
#define FFR_SPD 2
#define FFR_LS 29

// Flipper Front Left
#define FFL_FB 30
#define FFL_BRK 31
#define FFL_SPD 4
#define FFL_LS 26

// Flipper Back Right
#define FBR_FB 12
#define FBR_BRK 24
#define FBR_SPD 3
#define FBR_LS 28

// Flipper Back Left
#define FBL_FB 40
#define FBL_BRK 41
#define FBL_SPD 14
#define FBL_LS 27

#define LIGHT 7

int velocity[6];
int light_on;
bool light_switching;


void setup()
{
    pinMode(MR_FB, OUTPUT);
    pinMode(MR_BRK, OUTPUT); // break
    analogWriteFrequency(MR_SPD, 1000);

    pinMode(ML_FB, OUTPUT);
    pinMode(ML_BRK, OUTPUT);
    analogWriteFrequency(ML_SPD, 1000);

    pinMode(FFR_FB, OUTPUT);
    pinMode(FFR_BRK, OUTPUT);
    analogWriteFrequency(FFR_SPD, 1000);
    pinMode(FFR_LS, INPUT);

    pinMode(FFL_FB, OUTPUT);
    pinMode(FFL_BRK, OUTPUT);
    analogWriteFrequency(FFL_SPD, 1000);
    pinMode(FFL_LS, INPUT);

    pinMode(FBR_FB, OUTPUT);
    pinMode(FBR_BRK, OUTPUT);
    analogWriteFrequency(FBR_SPD, 1000);
    pinMode(FBR_LS, INPUT);

    pinMode(FBL_FB, OUTPUT);
    pinMode(FBL_BRK, OUTPUT);
    analogWriteFrequency(FBL_SPD, 1000);
    pinMode(FBL_LS, INPUT);

    pinMode(LIGHT, OUTPUT);

    velocity[0] = 0;
    velocity[1] = 0;
    velocity[2] = 0;
    velocity[3] = 0;
    velocity[4] = 0;
    velocity[5] = 0;
    light_on = 0;
    light_switching = false;

    driveMR(0);
    driveML(0);
    driveFFR(0);
    driveFFL(0);
    driveFBR(0);
    driveFBL(0);

    Serial.begin(115200);
    while (!Serial);
}

void loop()
{    
    if (Serial.available() > 0)
    {
        String incoming = Serial.readStringUntil('\n');
        incoming.trim();

        int count = 0;
        String temp = incoming;

        while (temp.length() > 0 && count < 7)
        {
            int idx = temp.indexOf(' ');
            String token = (idx == -1) ? temp : temp.substring(0, idx);
            
            if (count == 6) {
                if (token.toInt() && !light_switching)
                {
                    light_on = light_on ? 0 : 1;
                    light_switching = true;
                }
                else
                {
                    light_switching = false;
                }
            } else {
                velocity[count++] = token.toInt();
            }

            if (idx == -1)
                break;
            temp = temp.substring(idx + 1);
        }
        
        for (int i = 0; i < count; i++)
        {
            Serial.print("velocity ");
            Serial.print(i + 1);
            Serial.print(": ");
            Serial.print(velocity[i]);
            ;
            Serial.print(";"); // explicit carriage return + newline
        }
    }
    driveMR(velocity[0]);
    driveML(velocity[1]);
    
    if (digitalRead(FFR_LS) && velocity[2] < 0) driveFFR(0);
    else driveFFR(velocity[2]);

    if (digitalRead(FFL_LS) && velocity[3] > 0) driveFFL(0);
    else driveFFL(velocity[3]);

    if (digitalRead(FBR_LS) && velocity[4] > 0) driveFBR(0);
    else driveFBR(velocity[4]);

    if (digitalRead(FBL_LS) && velocity[5] < 0) driveFBL(0);
    else driveFBL(velocity[5]);
 
    digitalWrite(LIGHT, light_on);
}

void driveML(int spd)
{
    if (spd > 0)
    {
        analogWrite(ML_SPD, 255 - spd); // needs to be remap to 255-0 (255 is stop 0 is max)
        digitalWrite(ML_BRK, 0);
        digitalWrite(ML_FB, 0);
    }
    else if (spd < 0)
    {
        analogWrite(ML_SPD, 255 + spd);
        digitalWrite(ML_BRK, 0);
        digitalWrite(ML_FB, 1);
    }
    else
    {
        analogWrite(ML_SPD, 255);
        digitalWrite(ML_BRK, 1);
        digitalWrite(ML_FB, 0);
    }
}

void driveMR(int spd)
{
    if (spd > 0)
    {
        analogWrite(MR_SPD, 255 - spd);
        digitalWrite(MR_BRK, 0);
        digitalWrite(MR_FB, 0);
    }
    else if (spd < 0)
    {
        analogWrite(MR_SPD, 255 + spd);
        digitalWrite(MR_BRK, 0);
        digitalWrite(MR_FB, 1);
    }
    else
    {
        analogWrite(MR_SPD, 255);
        digitalWrite(MR_BRK, 1);
        digitalWrite(MR_FB, 0);
    }
}

void driveFBR(int spd)
{
    if (spd > 0)
    {
        analogWrite(FBR_SPD, 255 - spd);
        digitalWrite(FBR_BRK, 0);
        digitalWrite(FBR_FB, 0);
    }
    else if (spd < 0)
    {
        analogWrite(FBR_SPD, 255 + spd);
        digitalWrite(FBR_BRK, 0);
        digitalWrite(FBR_FB, 1);
    }
    else
    {
        analogWrite(FBR_SPD, 255);
        digitalWrite(FBR_BRK, 1);
        digitalWrite(FBR_FB, 0);
    }
}

void driveFFR(int spd)
{
    if (spd > 0)
    {
        analogWrite(FFR_SPD, 255 - spd);
        digitalWrite(FFR_BRK, 0);
        digitalWrite(FFR_FB, 0);
    }
    else if (spd < 0)
    {
        analogWrite(FFR_SPD, 255 + spd);
        digitalWrite(FFR_BRK, 0);
        digitalWrite(FFR_FB, 1);
    }
    else
    {
        analogWrite(FFR_SPD, 255);
        digitalWrite(FFR_BRK, 1);
        digitalWrite(FFR_FB, 0);
    }
}

void driveFFL(int spd)
{
    if (spd > 0)
    {
        analogWrite(FFL_SPD, 255 - spd);
        digitalWrite(FFL_BRK, 0);
        digitalWrite(FFL_FB, 0);
    }
    else if (spd < 0)
    {
        analogWrite(FFL_SPD, 255 + spd);
        digitalWrite(FFL_BRK, 0);
        digitalWrite(FFL_FB, 1);
    }
    else
    {
        analogWrite(FFL_SPD, 255);
        digitalWrite(FFL_BRK, 1);
        digitalWrite(FFL_FB, 0);
    }
}

void driveFBL(int spd)
{
    if (spd > 0)
    {
        analogWrite(FBL_SPD, 255 - spd);
        digitalWrite(FBL_BRK, 0);
        digitalWrite(FBL_FB, 0);
    }
    else if (spd < 0)
    {
        analogWrite(FBL_SPD, 255 + spd);
        digitalWrite(FBL_BRK, 0);
        digitalWrite(FBL_FB, 1);
    }
    else
    {
        analogWrite(FBL_SPD, 255);
        digitalWrite(FBL_BRK, 1);
        digitalWrite(FBL_FB, 0);
    }
}
