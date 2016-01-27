/* Augmented Pingpong Table
 *
 * Based on:
 * PingPong++
 * -------------
 * By Michael Bernstein (msbernst@mit.edu) and Xiao Xiao (x_x@mit.edu)
 */

// Constants
const int THRESHOLD = 30;

struct Hit {
  unsigned long upperLeft;
  unsigned long upperRight;
  unsigned long lowerLeft;
  unsigned long lowerRight;
  unsigned long centerLeft;
  unsigned long centerUp;
  unsigned long centerRight;
  unsigned long startTime;
  char side;
  boolean reported;  // have we sent it off via serial yet?
};

//Pin mapping of Teensy
int leftPins[] = {
  A8, A9, A10, A11, A12, A13, A14, A15};
int rightPins[] = {
  A0, A1, A2,  A3,  A4,  A5,  A6,  A7};

const unsigned long NO_RECORD = -1;
const unsigned long TIMEOUT_BETWEEN_HITS = 300000; // in millis
const char LEFT = 'l';
const char RIGHT = 'r';

// Variables
Hit curHit = { 
  NO_RECORD, NO_RECORD, NO_RECORD, NO_RECORD, NO_RECORD, NO_RECORD, NO_RECORD, NO_RECORD, LEFT, false};

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < 7; i++) {
    int pinNumber = leftPins[i];
    pinMode(pinNumber, INPUT);
    pinNumber = rightPins[i];
    pinMode(pinNumber, INPUT);
  }
}

void loop() {
  readPins(leftPins, LEFT);
  readPins(rightPins, RIGHT);
  
  if (isCompleteHit(&curHit) && !curHit.reported) {
    // print the current hit status
    Serial.print("hit: {");
    Serial.print(curHit.upperLeft);
    Serial.print(" ");
    Serial.print(curHit.upperRight);
    Serial.print(" ");
    Serial.print(curHit.lowerRight);
    Serial.print(" ");
    Serial.print(curHit.lowerLeft);
    Serial.print(" ");
    Serial.print(curHit.centerLeft);
    Serial.print(" ");
    Serial.print(curHit.centerUp);
    Serial.print(" ");
    Serial.print(curHit.centerRight);
    Serial.print(" ");
    Serial.print(curHit.side);
    Serial.println("}");
    
    curHit.reported = true;
  }

  if (hitTimedOut()) {
    // create a new hit
    Hit newHit;
    newHit.upperLeft = newHit.upperRight = newHit.lowerLeft = newHit.lowerRight = newHit.centerLeft = newHit.centerUp = newHit.centerRight = NO_RECORD;
    newHit.side = LEFT;
    newHit.startTime = NO_RECORD;
    newHit.reported = false;
    
    curHit = newHit;
  }
}

/*
 * For the list of one sides pins, see if any of them is detecting an analog reading above the threshold
 * and if so, report a hit with side and detection time
 */
void readPins(int* pinList, char curSide) {
  for (int i = 0; i < 7; i++) {
    int pinNumber = pinList[i];
    int pinValue = analogRead(pinNumber);
    if (pinValue >= THRESHOLD) {
      unsigned long detectionTime = micros();
      if (curHit.startTime == NO_RECORD) {
        curHit.startTime = detectionTime;
        curHit.side = curSide;
      }
      // add this data to the existing hit
      updateCorner(pinNumber, curSide, detectionTime, pinList);
     }
  }
}

/*
 * Updates the current hit data structure in the correct corner, given the pin number
 */
void updateCorner(int pinNumber, char curSide, unsigned long detectionTime, int* sidePins) {
  if (pinNumber == sidePins[0] && curHit.upperLeft == NO_RECORD) {
    curHit.upperLeft = detectionTime - curHit.startTime;
  }
  else if (pinNumber == sidePins[1] && curHit.upperRight == NO_RECORD) {
    curHit.upperRight = detectionTime - curHit.startTime;
  }
  else if (pinNumber == sidePins[2] && curHit.lowerRight == NO_RECORD) {
    curHit.lowerRight = detectionTime - curHit.startTime;
  }
  else if (pinNumber == sidePins[3] && curHit.lowerLeft == NO_RECORD) {
    curHit.lowerLeft = detectionTime - curHit.startTime;
  }
  else if (pinNumber == sidePins[4] && curHit.centerLeft == NO_RECORD) {
    curHit.centerLeft = detectionTime - curHit.startTime;
  }
  else if (pinNumber == sidePins[5] && curHit.centerUp == NO_RECORD) {
    curHit.centerUp = detectionTime - curHit.startTime;
  }
  else if (pinNumber == sidePins[6] && curHit.centerRight == NO_RECORD) {
    curHit.centerRight = detectionTime - curHit.startTime;
  }
}

boolean hitTimedOut() {
  unsigned long time_since = micros() - curHit.startTime;
  boolean timed_out = (time_since >= TIMEOUT_BETWEEN_HITS);
  return (curHit.startTime == NO_RECORD || timed_out);
}

boolean isCompleteHit(struct Hit *hit) {
  return hit->upperLeft != NO_RECORD && hit->upperRight != NO_RECORD && hit->lowerRight != NO_RECORD && hit->lowerLeft != NO_RECORD && hit->centerLeft != NO_RECORD && hit->centerUp != NO_RECORD && hit->centerRight != NO_RECORD;
}

