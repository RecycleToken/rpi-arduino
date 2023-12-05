#include <Servo.h>

#define SERVO_DELAY 400
#define GATE_PIN 11
#define HATCH_1_PIN 10
#define HATCH_2_PIN 9
#define HATCH_3_PIN 6
#define ECHO_PIN 3
#define TRIG_PIN 5
#define MAXIMUM_RANGE 400
#define MINIMUM_RANGE 2

Servo gate;
Servo hatch1;
Servo hatch2;
Servo hatch3;

String command;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  gate.attach(GATE_PIN);
  hatch1.attach(HATCH_1_PIN);
  hatch2.attach(HATCH_2_PIN);
  hatch3.attach(HATCH_3_PIN);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()) {
    command = Serial.readStringUntil('\n');
    command.trim();
    if (command.equals("1")) { //Command code from RPI
      recycle(hatch1);
    } else if (command.equals("2")) { //Command code from RPI
      recycle(hatch2);
    } else if (command.equals("3")) { //Command code from RPI
      recycle(hatch3);
    } else if (command.equals("4")) {
      recycle();
    } else {
      Serial.println("0"); // TODO: Handle 0 as error in RPI
    }
  } else {
    //TODO: send signal based on distance read
    int measurement = distance(MAXIMUM_RANGE, MINIMUM_RANGE);
    if(measurement < 10) {
      Serial.println("capture");
      delay(5000);
    }
  }
}

void recycle(Servo hatch) {
  hatch.write(180);
  delay(SERVO_DELAY); 
  gate.write(180);
  delay(SERVO_DELAY*2);
  gate.write(90);
  delay(SERVO_DELAY);
  hatch.write(90);
  delay(SERVO_DELAY);
}

void recycle() {
  gate.write(180);
  delay(SERVO_DELAY*2);
  gate.write(90);
  delay(SERVO_DELAY);
}

int distance(int maxrange, int minrange)
{
  long duration, distance;

  digitalWrite(TRIG_PIN,LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  duration = pulseIn(ECHO_PIN, HIGH);
  distance = duration / 58.2;
  delay(50);

  if(distance >= maxrange || distance <= minrange)
  return 0;
  return distance;
}
