#include <AccelStepper.h>

#define pul1 4
#define dir1 3
#define pul2 10
#define dir2 9

AccelStepper stepper1(1, pul1, dir1);
AccelStepper stepper2(1, pul2, dir2);

int motorSpeed = 1500;
int motorAccel = 10000;

int maxSpeed = 6000;
int maxAccel = 20000;
int stopTime = 30;

int start_x;
int start_y;

float circum = 4 * 3.1416;

bool commandReceived = false;

void interpolate(int steps_x, int steps_y);
void moveMotors(float x, float y);
void strike(float x, float y);
void sleep(float x, float y);
void otherSide(float x, float y);

void setup() {
  Serial.begin(9600);

  // Imposta la posizione iniziale dei motori
  stepper1.setCurrentPosition(0);
  stepper2.setCurrentPosition(0);

  stepper1.setMaxSpeed(motorSpeed);
  stepper2.setMaxSpeed(motorSpeed);
  stepper1.setAcceleration(motorAccel);
  stepper2.setAcceleration(motorAccel);

  while (!Serial.available()) {
  }

  // Legge i dati dalla seriale
  String sX = Serial.readStringUntil(' ');
  String sY = Serial.readStringUntil('\n');
  sX.trim();
  sY.trim();
  start_x = sX.toInt();
  start_y = sY.toInt();

  moveMotors(start_x, start_y);
  
  while (stepper1.isRunning() || stepper2.isRunning()) {
    stepper1.run();
    stepper2.run();
  }

  Serial.println("ready");
}

void loop() {

  String sX;
  String sY;
  String sCode;
  float x;
  float y;

  if (Serial.available() > 0 && !commandReceived) {

    sX = Serial.readStringUntil(' ');
    sY = Serial.readStringUntil(' ');
    sCode = Serial.readStringUntil('\n');
    sX.trim();
    sY.trim();
    sCode.trim();

    /*Serial.print("Hai inviato: ");
    Serial.print(sX);
    Serial.print(" "); 
    Serial.print(sY);
    Serial.print(" ");
    Serial.println(sCode);*/

    x = (float) sX.toInt();
    y = (float) sY.toInt();
    
    commandReceived = true;
  }
  
  if (commandReceived) {
    if (sCode == "move") {
      moveMotors(x, y);
    } else if (sCode == "strike") {
      strike(x, y);
    } else if (sCode == "sleep") {
      sleep(x, y);
    } else if (sCode == "otherSide") {
      otherSide(x, y);
    }
    commandReceived = false;
  }
  
  stepper1.run();
  stepper2.run();

}

/*void interpolate(int steps_x, int steps_y) {

  float stepRatio;
  int v1 = motorSpeed;
  int v2 = motorSpeed;
  int a1 = motorAccel;
  int a2 = motorAccel;

  int steps_xToGo = steps_x - stepper1.currentPosition();
  int steps_yToGo = steps_y - stepper2.currentPosition();

  if(steps_xToGo * steps_yToGo == 0) {

    stepper1.setMaxSpeed(motorSpeed);
    stepper1.setAcceleration(motorAccel);
    stepper2.setMaxSpeed(motorSpeed);
    stepper2.setAcceleration(motorAccel);

    /*Serial.print(stepRatio);
    Serial.print(" ");
    Serial.print(stepper1.maxSpeed());
    Serial.print(" ");
    Serial.print(stepper2.maxSpeed());
    Serial.print(" ");
    Serial.print(stepper1.acceleration());
    Serial.print(" ");
    Serial.println(stepper2.acceleration());

    return;

  }
  
  if (abs(steps_xToGo) >= abs(steps_yToGo)) {
  
    stepRatio = (float) abs(steps_yToGo) / abs(steps_xToGo);
    v2 = stepRatio * motorSpeed;
    a2 = stepRatio * motorAccel;
    
  } else {

    stepRatio = (float) abs(steps_xToGo) / abs(steps_yToGo);
    v1 = stepRatio * motorSpeed;
    a1 = stepRatio * motorAccel;
  }


  stepper1.setMaxSpeed(v1);
  stepper1.setAcceleration(a1);
  stepper2.setMaxSpeed(v2);
  stepper2.setAcceleration(a2);
  
  return;
}*/

void moveMotors(float x, float y) {

  x = (x / 800) * 60;
  y = (y / 800) * 60;

  // Conversione in passi per i motori
  float steps1x = (-x * 400 / circum);
  float steps1y = (-y * 400 / circum);
  float steps2x = (x * 400 / circum);
  float steps2y = (-y * 400 / circum);

  int steps1 = (steps1x + steps1y) / 2;
  int steps2 = (steps2x + steps2y) / 2;

  //interpolate(steps1, steps2);

  stepper1.moveTo(steps1);
  stepper2.moveTo(steps2);

  return;
}

void strike(float x, float y) {

  moveMotors(start_x, y);
  while(stepper1.isRunning() || stepper2.isRunning()) {
    stepper1.run();
    stepper2.run();
  }
  delay(stopTime);

  stepper1.setMaxSpeed(maxSpeed);
  stepper2.setMaxSpeed(maxSpeed);
  stepper1.setAcceleration(maxAccel);
  stepper2.setAcceleration(maxAccel);

  delay(stopTime);

  moveMotors(x, y);
  while(stepper1.isRunning() || stepper2.isRunning()) {
    stepper1.run();
    stepper2.run();
  }

  stepper1.setMaxSpeed(motorSpeed);
  stepper2.setMaxSpeed(motorSpeed);
  stepper1.setAcceleration(motorAccel);
  stepper2.setAcceleration(motorAccel);

  delay(stopTime);

  moveMotors(x, start_y);
  while(stepper1.isRunning() || stepper2.isRunning()) {
    stepper1.run();
    stepper2.run();
  }

  delay(stopTime);

  moveMotors(start_x, start_y);
  while(stepper1.isRunning() || stepper2.isRunning()) {
    stepper1.run();
    stepper2.run();
  }

  return;
}

void sleep(float x, float y) {

  stepper1.setMaxSpeed(motorSpeed);
  stepper2.setMaxSpeed(motorSpeed);
  stepper1.setAcceleration(motorAccel);
  stepper2.setAcceleration(motorAccel);
  while(stepper1.isRunning() || stepper2.isRunning()) {
    stepper1.run();
    stepper2.run();
  }
  
  moveMotors(0, 0);

  return;
}

void otherSide(float x, float y) {

  moveMotors(start_x, y);
  while(stepper1.isRunning() || stepper2.isRunning()) {
    stepper1.run();
    stepper2.run();
  }
  delay(stopTime);

  stepper1.setMaxSpeed(maxSpeed);
  stepper2.setMaxSpeed(maxSpeed);
  stepper1.setAcceleration(motorAccel);
  stepper2.setAcceleration(motorAccel);

  delay(stopTime);

  moveMotors(x, y);
  while(stepper1.isRunning() || stepper2.isRunning()) {
    stepper1.run();
    stepper2.run();
  }

  stepper1.setMaxSpeed(motorSpeed);
  stepper2.setMaxSpeed(motorSpeed);
  stepper1.setAcceleration(motorAccel);
  stepper2.setAcceleration(motorAccel);

  delay(stopTime);

  moveMotors(x, start_y);
  while(stepper1.isRunning() || stepper2.isRunning()) {
    stepper1.run();
    stepper2.run();
  }

  delay(stopTime);

  moveMotors(start_x, start_y);
  while(stepper1.isRunning() || stepper2.isRunning()) {
    stepper1.run();
    stepper2.run();
  }

  return;
}
