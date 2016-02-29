/*
 * Original PingPong++
 * -------------
 * By Michael Bernstein (msbernst@mit.edu) and Xiao Xiao (x_x@mit.edu)
 *
 * Augmented Table Tennis
 * -------------
 * By Andrea Amodeo and Erik Einebrant
 *
 * Continued by
 * -------------
 * Eloi Puertas
 * Oscar Bañó
 * Jordi Serres
 * Albert Sansó
 
 */

// Constants
const int THRESHOLD = 4;
const int SENSOR_COUNT = 8;
//NOTE: There are 8 but for the time being we only use 7 as this is more compatible with available software

struct Hit {
  unsigned long timings[SENSOR_COUNT];
  int volumes[SENSOR_COUNT];

  unsigned long startTime;
  char side;
  boolean reported;  // have we sent it off via serial yet?
};

//Pin mapping of Teensy
int rightPins[] = { A8, A9, A10, A11, A12, A13, A14, A15}; // clockwise from top left
int leftPins[] = { A0, A1, A2, A3, A4, A5, A6, A7}; // clockwise from top left
int rightThresholds[] = {10, 4, 4, 4, 4, 4, 4, 10};
int leftThresholds[] = {4, 4, 4, 4, 4, 4, 4, 10};

const unsigned long NO_RECORD = -1;
const unsigned long TIMEOUT_BETWEEN_HITS = 10000; // in micros
const char LEFT = 'l';
const char RIGHT = 'r';
const char UNDEF = 'u';
Hit curHit;


void setup() {
  createNewHit();
  Serial.begin(115200);
}

void loop() {
  //delay(5);
  if (curHit.side == UNDEF || curHit.side == LEFT) {
      readPins(leftPins, leftThresholds, LEFT);
    }
  if (curHit.side == UNDEF || curHit.side == RIGHT){
      readPins(rightPins, rightThresholds, RIGHT);
    }
}

  //Serial.println(curHit.volumes[0]);

  if (isCompleteHit(&curHit) && !curHit.reported) {
    // print the current hit status
    Serial.print("hit: {");
    for (int i = 0; i < SENSOR_COUNT; i++) {
      Serial.print(curHit.timings[i]);
      Serial.print(":");
      Serial.print(curHit.volumes[i]);
      Serial.print(" ");
    }
    Serial.print(curHit.side);
    Serial.println("}");

    curHit.reported = true;
  }

  if (hitTimedOut()) {
    createNewHit();
  }
}


void createNewHit() {
  // create a new hit
  Hit newHit;
  for (int i = 0; i < SENSOR_COUNT; i++) {
    newHit.timings[i] = NO_RECORD;
    newHit.volumes[i] = NO_RECORD;
  }

  newHit.side = UNDEF;
  newHit.startTime = NO_RECORD;
  newHit.reported = false;

  curHit = newHit;
}

/*
 * For the list of one sides pins, see if any of them is detecting an analog reading above the threshold
 * and if so, report a hit with side and detection time
 */
void readPins(int* pinList, int* thresholds, char curSide) {
  for (int i = 0; i < SENSOR_COUNT; i++) {
    int pinNumber = pinList[i];
    int pinValue = analogRead(pinNumber);
    //Serial.println(pinValue);
    if (pinValue >= thresholds[i]) {
      unsigned long detectionTime = micros();
      if (curHit.startTime == NO_RECORD) {
        curHit.startTime = detectionTime;
        curHit.side = curSide;
      }
      // add this data to the existing hit
      updateCorner(pinNumber, curSide, detectionTime, pinValue, pinList);
    }
  }
}

/*
 * Updates the current hit data structure in the correct corner, given the pin number
 */
void updateCorner(int pinNumber, char curSide, unsigned long detectionTime, int pinValue, int* sidePins) {
  for (int i = 0; i < SENSOR_COUNT; i++) {
    if (pinNumber == sidePins[i] && curHit.timings[i] == NO_RECORD) {
      curHit.timings[i] = detectionTime - curHit.startTime;
      curHit.volumes[i] = pinValue;
    }
  }
}

boolean hitTimedOut() {
  unsigned long time_since = micros() - curHit.startTime;
  boolean timed_out = (time_since >= TIMEOUT_BETWEEN_HITS);
  return (curHit.startTime == NO_RECORD || timed_out);
}

boolean isCompleteHit(struct Hit *hit) {
  boolean isHit = true;
  for (int i = 0; i < SENSOR_COUNT; i++) {
    isHit = isHit && hit->timings[i] != NO_RECORD;
  }
  return isHit;
}

