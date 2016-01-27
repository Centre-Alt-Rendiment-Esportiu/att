int knockSensor = 1;
int val0 = 0;
int val1 = 0;
int THRESHOLD = 5;

void setup() {
  Serial.begin(115200);
}

void loop() {
  val0 = analogRead(7);

  
  if (val0 >= THRESHOLD ) {
    
    
    Serial.print("( ");
    Serial.print(val0);
    //Serial.print(", ");
    //Serial.print(val1);
    Serial.println(")");
    
    
    /*
    int r = val0-val1;
    Serial.println(r);
    */
  }
  //delay(100);  // we have to make a delay to avoid overloading the serial port
}
