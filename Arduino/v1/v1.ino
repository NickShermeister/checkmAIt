#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 90;    // variable to store the servo position

const int UP_POS = 60;
const int DOWN_POS = 140;

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0){
    int msg = Serial.read();

    if (msg == 'U' || msg == 'u'){
      pos = UP_POS;
    }
     
    if (msg == 'D' || msg == 'd'){
      pos = DOWN_POS;
    }
  }
  myservo.write(pos);
  return;
  
  myservo.write(DOWN_POS);
  delay(1500);
  
  myservo.write(UP_POS);
  delay(1000);
}

