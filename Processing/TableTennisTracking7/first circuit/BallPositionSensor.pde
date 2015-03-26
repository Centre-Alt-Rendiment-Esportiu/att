 import matrixMath.*;

import processing.serial.*;

class BallPositionSensor {
  boolean debug = false;
  int TABLE_WIDTH = 60;   // inches
  int TABLE_HEIGHT = 54;  // inches
  
  Serial arduinoSerial;
  matrixMath mc1_l, mc2_l, mc3_l, mc4_l, mc5_l, mc6_l, mc1_r, mc2_r, mc3_r, mc4_r, mc5_r, mc6_r;
  
  BallPositionSensor(PApplet applet, String portName, String coefficientFileLeft, String coefficientFileRight) {
    importCoeffs(coefficientFileLeft, false); // "../../coefficients-left.txt"
    importCoeffs(coefficientFileRight, true); // "../../coefficients-right.txt"
    arduinoSerial = new Serial(applet, portName, 115200);
  }

  void importCoeffs(String coefficientFile, boolean isRightSide) {
    String[] coeffs = loadStrings(coefficientFile);

    float[][] coeffs1 = new float[2][21];
    float[][] coeffs2 = new float[2][21];
    float[][] coeffs3 = new float[2][21];
    float[][] coeffs4 = new float[2][21];
    float[][] coeffs5 = new float[2][21];
    float[][] coeffs6 = new float[2][21];
    for (int i = 0; i < 21; i++) {
      coeffs1[0][i] = float(coeffs[i]);
      coeffs2[0][i] = float(coeffs[21+i]);
      coeffs3[0][i] = float(coeffs[42+i]);
      coeffs4[0][i] = float(coeffs[63+i]);
      coeffs5[0][i] = float(coeffs[84+i]);
      coeffs6[0][i] = float(coeffs[105+i]);
      
      coeffs1[1][i] = float(coeffs[126+i]); 
      coeffs2[1][i] = float(coeffs[147+i]);
      coeffs3[1][i] = float(coeffs[168+i]);
      coeffs4[1][i] = float(coeffs[189+i]);
      coeffs5[1][i] = float(coeffs[210+i]);
      coeffs6[1][i] = float(coeffs[231+i]);
    }
    if (isRightSide) { 
      mc1_r = new matrixMath(coeffs1); 
      mc2_r = new matrixMath(coeffs2);
      mc3_r = new matrixMath(coeffs3);
      mc4_r = new matrixMath(coeffs4);
      mc5_r = new matrixMath(coeffs5);
      mc6_r = new matrixMath(coeffs6);
    }
    else {
      mc1_l = new matrixMath(coeffs1);
      mc2_l = new matrixMath(coeffs2);
      mc3_l = new matrixMath(coeffs3);
      mc4_l = new matrixMath(coeffs4);
      mc5_l = new matrixMath(coeffs5);
      mc6_l = new matrixMath(coeffs6);
    }
  }

  Hit readHit() {
     String serialData = null;
     if (debug) {
       if (random(100) <= 1) {
         serialData = "hit: {1908 1120 0 2004 1700 98 r}";
       } else if (random(100) <= 1) {
         serialData = "hit: {1544 668 0 1288 1700 569 r}";
       }
       else {
         serialData = null;
       }
     } else if (arduinoSerial.available() > 0) {
       serialData = arduinoSerial.readStringUntil(10);  //10 is character for linefeed
     }  


    if (serialData == null) {
      return null;
    }
    else {
      println(serialData);
      Hit hit = getHit(serialData);
      // 54 x 60
      //println("(" + position.x + ", " + position.y + ")");
      return hit;
    }
  }

  private Hit getHit(String serialData) {
    String[] values = split(serialData, "{");
    String[] timings = split(values[1], " ");

    float t12 = float(timings[0])-float(timings[1]);
    float t13 = float(timings[0])-float(timings[2]);
    float t14 = float(timings[0])-float(timings[3]);
    float t15 = float(timings[0])-float(timings[4]);
    float t16 = float(timings[0])-float(timings[5]);
    float t23 = float(timings[1])-float(timings[2]);
    float t24 = float(timings[1])-float(timings[3]);
    float t25 = float(timings[1])-float(timings[4]);
    float t26 = float(timings[1])-float(timings[5]);
    float t34 = float(timings[2])-float(timings[3]);
    float t35 = float(timings[2])-float(timings[4]);
    float t36 = float(timings[2])-float(timings[5]);
    float t45 = float(timings[3])-float(timings[4]);
    float t46 = float(timings[3])-float(timings[5]);
    float t56 = float(timings[4])-float(timings[5]);
     
    /*int first_one = 0;
    int first_two = 0; 
    int first_four = 0;
    if (int(timings[0]) == 0) {
      first_one = 1;
    } else if (int(timings[1]) == 0) {
      first_two = 1;
    } else if (int(timings[3]) == 0) {
      first_four = 1;
    }*/

    float[] timings1 = {
      pow(t12,2), pow(t13,2), pow(t14,2), pow(t15,2), pow(t16,2),
      t12*t13, t12*t14, t12*t15, t12*t16, t13*t14, t13*t15, t13*t16, t14*t15, t14*t16, t15*t16, t12, t13, t14, t15, t16, 1};
    float[] timings2 = {
      pow(t12,2), pow(t23,2), pow(t24,2), pow(t25,2), pow(t26,2), 
      t12*t23, t12*t24, t12*t25, t12*t26, t23*t24, t23*t25, t23*t26, t24*t25, t24*t26, t25*t26, t12, t23, t24, t25, t26, 1};
    float[] timings3 = {
      pow(t13,2), pow(t23,2), pow(t34,2), pow(t35,2), pow(t36,2), 
      t13*t23, t13*t34, t13*t35, t13*t36, t23*t34, t23*t35, t23*t36, t34*t35, t34*t36, t35*t36, t13, t23, t34, t35, t36, 1};
    float[] timings4 = {
      pow(t14,2), pow(t24,2), pow(t34,2), pow(t45,2), pow(t46,2),
      t14*t24, t14*t34, t14*t45, t14*t46, t24*t34, t24*t45, t24*t46, t34*t45, t34*t46, t45*t46, t14, t24, t34, t45, t46, 1};
    float[] timings5 = {
      pow(t15,2), pow(t25,2), pow(t35,2), pow(t45,2), pow(t56,2),
      t15*t25, t15*t35, t15*t45, t15*t56, t25*t35, t25*t45, t25*t56, t35*t45, t35*t56, t45*t56, t15, t25, t35, t45, t56, 1};  
    float[] timings6 = {
      pow(t16,2), pow(t26,2), pow(t36,2), pow(t46,2), pow(t56,2),
      t16*t26, t16*t36, t16*t46, t16*t56, t26*t36, t26*t46, t26*t56, t36*t46, t36*t56, t46*t56, t16, t26, t36, t46, t56, 1};
      
    PVector guess1 = null;
    PVector guess2 = null;
    PVector guess3 = null;
    PVector guess4 = null;
    PVector guess5 = null;
    PVector guess6 = null;
   
    boolean isRightSide = false;
    if (serialData.contains("r}")) {
      isRightSide = true; 
      guess1 = calcXY(timings1, mc1_r);
      guess2 = calcXY(timings2, mc2_r);
      guess3 = calcXY(timings3, mc3_r);
      guess4 = calcXY(timings4, mc4_r);
      guess5 = calcXY(timings5, mc5_r);
      guess6 = calcXY(timings6, mc6_r);
    } else if (serialData.contains("l}")) {
      guess1 = calcXY(timings1, mc1_l);
      guess2 = calcXY(timings2, mc2_l);
      guess3 = calcXY(timings3, mc3_l);
      guess4 = calcXY(timings4, mc4_l);
      guess5 = calcXY(timings5, mc5_l);
      guess6 = calcXY(timings6, mc6_l);
      isRightSide = false;
    }
    
    println("guess 1: " + guess1.x + ", " + guess1.y);
    println("guess 2: " + guess2.x + ", " + guess2.y);
    println("guess 3: " + guess3.x + ", " + guess3.y);
    println("guess 4: " + guess4.x + ", " + guess4.y);
    println("guess 5: " + guess5.x + ", " + guess5.y);
    println("guess 6: " + guess6.x + ", " + guess6.y);
    
    float x_inches = (guess1.x+guess2.x+guess3.x+guess4.x+guess5.x+guess6.x)/6;
    float y_inches = (guess1.y + guess2.y + guess3.y + guess4.y + guess5.y + guess6.y)/6;
    println(x_inches + ", " + y_inches);

    return new Hit(x_inches, y_inches, isRightSide, TABLE_WIDTH, TABLE_HEIGHT);
  }

  PVector calcXY(float[] timings, matrixMath mc) {
    matrixMath result = matrixMath.columnMultiplyMatrix(timings, mc);    
    float x = Math.max(0, Math.min(TABLE_WIDTH, result.getNumber(0, 0)));
    float y = Math.max(0, Math.min(TABLE_HEIGHT, result.getNumber(0, 1)));
    return new PVector(x, y);
  }

}

