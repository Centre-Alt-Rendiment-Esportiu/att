int knockSensor = 1;
int val0 = 0;
int val1 = 0;
int val2 = 0;
int val3 = 0;
int val4 = 0;
int val5 = 0;
int val6 = 0;
int val7 = 0;
int THRESHOLD = 1;

void setup() {
  Serial.begin(115200);
}

void loop() {
  val0 = analogRead(A0);
  val1 = analogRead(A1);
  val2 = analogRead(A2);
  val3 = analogRead(A3);
  val4 = analogRead(A4);
  val5 = analogRead(A5);
  val6 = analogRead(A6);
  val7 = analogRead(A7);

  /*
  if (val0 >= THRESHOLD || val1 >= THRESHOLD || val2 >= THRESHOLD ||  val3 >= THRESHOLD 
    || val4 >= THRESHOLD || val5 >= THRESHOLD || val6 >= THRESHOLD || val7 >= THRESHOLD ) {
    */

  if (val0 >= THRESHOLD || val1 >= THRESHOLD || val2 >= THRESHOLD ||  val3 >= THRESHOLD 
    || val4 >= THRESHOLD || val5 >= THRESHOLD || val6 >= THRESHOLD || val7 >= THRESHOLD ) {

    Serial.print("( ");
    Serial.print(val0);
    Serial.print(", ");
    Serial.print(val1);
    Serial.print(", ");
    Serial.print(val2);
    Serial.print(", ");
    Serial.print(val3);
    Serial.print(", ");
    Serial.print(val4);
    Serial.print(", ");
    Serial.print(val5);
    Serial.print(", ");
    Serial.print(val6);
    Serial.print(", ");
    Serial.print(val7);
    Serial.println(")");
    
    
    /*
    int r = val0-val1;
    Serial.println(r);
    */
  }
  delay(50);  // we have to make a delay to avoid overloading the serial port
}
