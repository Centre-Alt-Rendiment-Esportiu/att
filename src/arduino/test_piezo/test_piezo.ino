/* Piezo Test
 *
 * Based on:
 * http://www.arduino.cc/en/Tutorial/Knock  
 */

// Constants
const int LED_PIN    = 13;
const int SENSOR_PIN = A8;
const int THRESHOLD  = 5;

// Variables
long lastTime = 0;
int deltaTime = 0;
int timer = 0;
int sensorReading = 0;      // variable to store the value read from the sensor pin

void setup() {
 pinMode(LED_PIN, OUTPUT); // declare the ledPin as as OUTPUT
 Serial.begin(115200);       // use the serial port
}

void loop() {
  long curTime = millis();
  deltaTime = curTime - lastTime;
  lastTime = curTime;
  
  // read the sensor and store it in the variable sensorReading:
  sensorReading = analogRead(SENSOR_PIN);
 
  // if the sensor reading is greater than the threshold:
  if (sensorReading >= THRESHOLD) {
    // Flash the led for 10ms
    timer = 10;
    digitalWrite(LED_PIN, HIGH);
  }
  
  //Update delta time
  timer -= deltaTime;
  
  //Timeout led
  if(timer <= 0){
    timer = 0;
    digitalWrite(LED_PIN, LOW);
  }
  
  //Serial.println(sensorReading);
  //delay(2);  // delay to avoid overloading the serial port buffer
}
