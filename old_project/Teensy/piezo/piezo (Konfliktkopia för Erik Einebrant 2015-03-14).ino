/* Knock Sensor
 
   This sketch reads a piezo element to detect a knocking sound.
   It reads an analog pin and compares the result to a set threshold.
   If the result is greater than the threshold, it writes
   "knock" to the serial port, and toggles the LED on pin 13.
 
   The circuit:
    * + connection of the piezo attached to analog in 0
    * - connection of the piezo attached to ground
    * 1-megohm resistor attached from analog in 0 to ground

   http://www.arduino.cc/en/Tutorial/Knock
   
   created 25 Mar 2007
   by David Cuartielles <http://www.0j0.org>
   modified 30 Aug 2011
   by Tom Igoe
   
   This example code is in the public domain.

 */


// these constants won't change:
const int ledPin = 13;      // led connected to digital pin 13
const int knockSensor = A0; // the piezo is connected to analog pin 0
const int knockSensor2 = A1; // the piezo is connected to analog pin 0
const int threshold = 10;  // threshold value to decide when the detected sound is a knock or not


// these variables will change:
long lastTime = 0;
int deltaTime = 0;
int timer = 0;
int sensorReading = 0;      // variable to store the value read from the sensor pin
int sensorReading2 = 0;
int ledState = LOW;         // variable used to store the last LED status, to toggle the light

void setup() {
 pinMode(ledPin, OUTPUT); // declare the ledPin as as OUTPUT
 Serial.begin(115200);       // use the serial port
}

void loop() {
  long curTime = millis();
  deltaTime = curTime - lastTime;
  lastTime = curTime;
  
  // read the sensor and store it in the variable sensorReading:
  sensorReading = analogRead(knockSensor);
  //sensorReading2 = analogRead(knockSensor2);
 
  // if the sensor reading is greater than the threshold:
  if (sensorReading >= threshold /*|| sensorReading2 >= threshold*/) {
    // toggle the status of the ledPin:
    //ledState = HIGH;
    timer = 10;
    // update the LED pin itself:
    digitalWrite(ledPin, HIGH);
    // send the string "Knock!" back to the computer, followed by newline
    
  }
  
  timer -= deltaTime;
  
  if(timer <= 0){
    timer = 0;
    digitalWrite(ledPin, LOW);
  }
  //Serial.println(sensorReading);
  //delay(5);  // delay to avoid overloading the serial port buffer
}
