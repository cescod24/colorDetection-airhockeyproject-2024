#include <AccelStepper.h>

#define pul1 4
#define dir1 3
#define pul2 10
#define dir2 9

int forward = 400;
int backwards = -400;

AccelStepper stepper1(1, pul1, dir1);
AccelStepper stepper2(1, pul2, dir2);


int motorSpeed = 1000;
int motorAccel = 11000;

int threshold = 20;


void setup() {
  
  Serial.begin(9600);

  stepper1.setMaxSpeed(motorSpeed);
  stepper1.setAcceleration(motorAccel);
  stepper1.setCurrentPosition(0);
  
  stepper2.setMaxSpeed(motorSpeed);
  stepper2.setAcceleration(motorAccel);
  stepper2.setCurrentPosition(0);

  Serial.println("Preparazione completata");

}

void loop() {

  int target1;
  int target2;
  int stepsGoalie = -1;

  bool defenseMode = false;
  bool defAndAttackMode = true;
  bool hitting = false;

  if (Serial.available() > 0) {

    String center_x;
    String center_y;
    String acceleration;
    
    String goalDet = Serial.readStringUntil('\n');
    goalDet.trim();


    if(goalDet == "none") {

      Serial.println("return to zero");

      if (defenseMode) {
        target1 = 0;
        target2 = 0;  
      }
      

    } else {

      String center_x = Serial.readStringUntil('\n');
      String center_y = Serial.readStringUntil('\n');
      String acceleration = Serial.readStringUntil('\n');
      center_x.trim();
      center_y.trim();
      acceleration.trim();
      Serial.print("goal at: ");
      Serial.print(goalDet);
      Serial.print(", center_x: ");
      Serial.print(center_x);
      Serial.print(", center_y: ");
      Serial.print(center_y);
      Serial.print(", acceleration: ");
      Serial.println(acceleration);

    }
    
    if(goalDet.toInt() != 0) {

      int goalObj = goalDet.toInt();
      stepsGoalie = goalObj * 1.125 - 450;

      if(abs(stepsGoalie - target1) > threshold || -threshold < stepsGoalie < threshold ) {

        target1 = stepsGoalie;
        target2 = stepsGoalie;

        stepper1.moveTo(target1);
        stepper2.moveTo(target2);

        while(stepper1.isRunning() || stepper2.isRunning()) {
          stepper1.run();
          stepper2.run();
        }

        target1 -= forward;
        target2 += forward;
        
        stepper1.moveTo(target1);
        stepper2.moveTo(target2);

        while(stepper1.isRunning() || stepper2.isRunning()) {

          stepper1.run();
          stepper2.run();
        }

        target1 -= backwards;
        target2 += backwards;
        
        stepper1.moveTo(target1);
        stepper2.moveTo(target2);

        while(stepper1.isRunning() || stepper2.isRunning()) {

          stepper1.run();
          stepper2.run();
        }

        target1 = 0;
        target2 = 0;
        
        stepper1.moveTo(target1);
        stepper2.moveTo(target2);

        while(stepper1.isRunning() || stepper2.isRunning()) {

          stepper1.run();
          stepper2.run();
        }
      }
    }

  }
  

} 