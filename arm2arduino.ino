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
  inputString.reserve(200);  // Reserve space for input string
  Serial.println("Setup complete. Waiting for commands...");
}

void loop() {
  if (stringComplete) {
    processCommands(inputString);
    inputString = "";
    stringComplete = false;
  }
}

void processCommands(String commandString) {
  int startIndex = 0;
  int endIndex = 0;
  
  while ((endIndex = commandString.indexOf('\n', startIndex)) != -1) {
    String command = commandString.substring(startIndex, endIndex);
    executeCommand(command);
    startIndex = endIndex + 1;
  }
}

void executeCommand(String command) {
  if(command.startsWith("S")) {
    int servoNum = command.substring(1, command.indexOf(',')).toInt();
    int angle = map(command.substring(command.indexOf(',') + 1).toInt(), 0, 180, SERVOMIN, SERVOMAX);
    
    Serial.print("Executing command for servo ");
    Serial.print(servoNum);
    Serial.print(" to angle: ");
    Serial.println(angle);
    pwm.setPWM(servoNum, 0, angle);
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
