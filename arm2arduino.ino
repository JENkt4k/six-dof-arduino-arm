#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>


Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
String inputString = ""; 
bool stringComplete = false;
int SERVOMIN = 125;
int SERVOMAX = 500;

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(60);
  inputString.reserve(10);  // Reserve space for input string
  
  Serial.println("Setup complete. Waiting for commands...");
}

void loop() {
  if (stringComplete) {
    Serial.print("Received: ");
    Serial.println(inputString);

    if(inputString.startsWith("S")) {
      int servoNum = inputString.substring(1,2).toInt();
      int angle = map(inputString.substring(3).toInt(), 0, 180, SERVOMIN, SERVOMAX);
      
      Serial.print("Setting servo ");
      Serial.print(servoNum);
      Serial.print(" to angle: ");
      Serial.println(angle);

      pwm.setPWM(servoNum, 0, angle);
    }
    
    inputString = "";
    stringComplete = false;
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
