import processing.serial.*;
import java.util.*;
import java.awt.Frame;
import gifAnimation.*;


SecondScreen computerScreen;

String winSerial = "COM14";
String macSerial = "/dev/tty.usbserial-A9005d9p";
float screenMultiplier = 9.4;
float CM_TO_IN = 0.393700787;

BallPositionSensor sensor;


//Constants ms and inch
int TIMEOUT = 2000;

int MAIN_MENU = 0;
int TARGET = 1;
int SERVICE = 2;
int POINT_PATTERN = 3;
int mode = MAIN_MENU;
Mode[] modes = new Mode[4];

Gif trainingGif;

boolean debug;

void setup() {
  size(int(2 * 54 * screenMultiplier), int(60 * screenMultiplier));
  colorMode(RGB, 255, 255, 255, 100);

  trainingGif = new Gif(this, "training.gif");
  trainingGif.loop();

  modes[0] = new MainMenu();
  modes[1] = new Target();
  modes[2] = new Service();
  modes[3] = new Pattern();

  debug = false;

  sensor = new BallPositionSensor(this, winSerial, "data/coefficients-left.txt", "data/coefficients-right.txt");
  
  PFrame f = new PFrame();
  
  smooth();
}

void draw() {  

  Hit hit = sensor.readHit();
  if (hit != null) {
    onHit(hit);
  }

  modes[mode].display();
}

void onHit(Hit hit) {
  modes[mode].onHit(hit);
}

float distance(Hit h1, Hit h2) {
  if (h1 != null && h2 != null) {
    return dist(h1.x, h1.y, h2.x, h2.y);
  }
  return 1000;
}

//setting up the computer screen
public class PFrame extends Frame {
  public PFrame() {
    setBounds(0, 0, displayWidth, displayHeight);
    computerScreen = new SecondScreen();
    add(computerScreen);
    computerScreen.init();
    show();
  }
}

public class SecondScreen extends PApplet {
  public void setup() {
    size(displayWidth, displayHeight);
  }

  public void draw() {
    modes[mode].secondDisplay();
  }

  void mouseClicked() {
    modes[mode].onMouseClicked();
  }
}

Hit mouse2hit(float mx, float my) {
  float x = my / screenMultiplier;
  float y = mx % (54 * screenMultiplier) / screenMultiplier;
  boolean hitRightSide = mx > 54 * screenMultiplier;
  if (hitRightSide) {
    x = 60 - x;
    y = 54 - y;
  }
  return new Hit(x, y, hitRightSide, 60, 54);
}

void mouseClicked() {
  colorMode(RGB);
  modes[mode].onMouseClicked();
}

void drawButtons(int[][] continueModifyBox, String[] continueModify) {
  computerScreen.textAlign(CENTER);
  for (int i=0; i<2; i++) { // modify or continue bottons
    computerScreen.rect(continueModifyBox[i][0], continueModifyBox[i][1], continueModifyBox[i][2], continueModifyBox[i][3], continueModifyBox[i][4]);
    computerScreen.text(continueModify[i], continueModifyBox[i][0], continueModifyBox[i][1]+30, continueModifyBox[i][2], continueModifyBox[i][3]);
  }
  for (int i=0; i<2; i++) { // highlights the buttons
    if ((computerScreen.mouseX > continueModifyBox[i][0] && computerScreen.mouseX < continueModifyBox[i][0] + continueModifyBox[i][2]) && 
      (computerScreen.mouseY > continueModifyBox[i][1] && computerScreen.mouseY < continueModifyBox[i][1] + continueModifyBox[i][3])) {
      computerScreen.stroke(255);
      computerScreen.fill(#8E8B89);
      computerScreen.rect(continueModifyBox[i][0], continueModifyBox[i][1], continueModifyBox[i][2], continueModifyBox[i][3], continueModifyBox[i][4]);
      computerScreen.fill(255);
      computerScreen.text(continueModify[i], continueModifyBox[i][0], continueModifyBox[i][1]+30, continueModifyBox[i][2], continueModifyBox[i][3]);
      computerScreen.noFill();
    }
  }
}

void debugMouse() {
  if (debug) {
    println("click");
    float x = mouseY / screenMultiplier;
    float y = mouseX % (54 * screenMultiplier) / screenMultiplier;
    boolean hitRightSide = mouseX > 54 * screenMultiplier;
    if (hitRightSide) {
      x = 60 - x;
      y = 54 - y;
    }
    modes[mode].onHit(new Hit(x, y, hitRightSide, 60, 54));
  }
}

void keyPressed(){
  modes[mode].onKeyPressed();
}

