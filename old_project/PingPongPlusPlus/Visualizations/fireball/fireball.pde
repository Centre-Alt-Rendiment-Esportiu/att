/**
 * Fireball
 * 
 * by Xiao Xiao (x_x@mit.edu) and Michael Bernstein (msbernst@mit.edu) 
 * based on Smoke Particle System sketch by Daniel Shiffman.  
 *  
 */

import processing.serial.*;

ParticleSystem ps;
Random generator;

PVector destPosition;

float rho = 1;

String winSerial = "COM7";
String macSerial = "/dev/tty.usbserial-A6008cmo";

BallPositionSensor sensor;
BallPositionUploader uploader;

float screenMultiplier = 11;

void setup() {
  size(int(2*54*screenMultiplier), int(60*screenMultiplier));
  colorMode(RGB, 255, 255, 255, 100);
  background(0);

  sensor = new BallPositionSensor(this, macSerial, "../../coefficients-left.txt", "../../coefficients-right.txt");
  uploader = new BallPositionUploader("Media Lab");    

  // Using a Java random number generator for Gaussian random numbers
  generator = new Random();

  // Create an alpha masked image to be applied as the particle's texture
  PImage msk = loadImage("texture.gif");
  PImage img = new PImage(msk.width,msk.height);
  for (int i = 0; i < img.pixels.length; i++) img.pixels[i] = color(255);
  img.mask(msk);
  ps = new ParticleSystem(0, new PVector(width/2, height/2),img);
  
  destPosition = ps.getOrigin();;
  smooth();
}

void draw() {
  background(0);

  noFill();
  stroke(200, 100, 100, 200);
  ellipse (destPosition.x, destPosition.y, 44, 44);
  ellipse (destPosition.x, destPosition.y, 43, 43);
  ellipse (destPosition.x, destPosition.y, 42, 42);
  ellipse (destPosition.x, destPosition.y, 41, 41);
  ellipse (destPosition.x, destPosition.y, 40, 40);
  
  PVector origin = ps.getOrigin();  
  Hit ballLocation = sensor.readHit();
  if (ballLocation != null) {
    rho = 1;
    destPosition = ballLocation.getPixelVector();
  }

  if (origin.x != destPosition.x) {
    ps.setOrigin(new PVector(origin.x*rho + (1-rho) * destPosition.x,
                 origin.y*rho + (1-rho) * destPosition.y));
    rho -= 0.02;

    float dx = (origin.x - destPosition.x)/500;
    float dy = (origin.y - destPosition.y)/500;
    PVector wind = new PVector(dx,dy,0); 
    ps.add_force(wind);
  }
  
  ps.run();
  for (int i = 0; i < 10; i++) {
    ps.addParticle();
  }
}

void mouseClicked() {
   destPosition = new PVector(mouseX, mouseY);
   rho = 1;
}










