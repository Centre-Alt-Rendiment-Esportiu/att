import java.util.*;
import gifAnimation.*;

class Pattern extends Mode {
  PVector destPosition;
  ArrayList<Ball> training;
  Ball lastBall;
  int nLines; 
  boolean isPoint;
  boolean playerOneIsRightSide;
  boolean isDoubleHit;
  boolean interpoleWhiteFlag;

  Pattern() {
    colorMode(RGB);
    destPosition = new PVector(0, 0);
    training = new ArrayList<Ball>();
    nLines = 0;
    isPoint = false;
    playerOneIsRightSide = false;
    isDoubleHit = false;
    interpoleWhiteFlag = false;
  }

  void display() {
    background(0);
    if (isPoint) {
      showLastPoint();
      //debug = false;
    }
    else {
      //debug = true;
      checkTimeout();
    }
  }

  void secondDisplay() {
    int[] mainMenuBox = { 
      computerScreen.width/2-200, computerScreen.height - 150, 400, 100, 7
    };

    int[][] continueModifyBox = { 
      {
        computerScreen.width/2 - 605, computerScreen.height - 150, 400, 100, 7
      }
      , 
      {
        computerScreen.width/2 + 205, computerScreen.height - 150, 400, 100, 7
      }
    };

    String[] continueModify = { 
      "Main Menu", "Repeat"
    };

    PFont verdana60 = loadFont("Verdana-60.vlw");
    PFont verdana48 = loadFont("Verdana-48.vlw");
    PFont verdana36 = loadFont("Verdana-36.vlw");

    computerScreen.background(0);

    computerScreen.fill(255);
    computerScreen.textAlign(CENTER);
    computerScreen.textFont(verdana60);
    computerScreen.text("Point's Pattern", 0, 50, computerScreen.width, computerScreen.height);
    computerScreen.textFont(verdana48);

    if (!isPoint) {
      computerScreen.text("Play a Point", 0, 200, computerScreen.width, 50);

      //quit training button
      computerScreen.stroke(255);
      computerScreen.noFill();
      computerScreen.rect(mainMenuBox[0], mainMenuBox[1], mainMenuBox[2], mainMenuBox[3], mainMenuBox[4]);
      computerScreen.text("Quit Training", mainMenuBox[0], mainMenuBox[1]+30, mainMenuBox[2], mainMenuBox[3]);
      if ((computerScreen.mouseX > mainMenuBox[0] && computerScreen.mouseX < mainMenuBox[0] + mainMenuBox[2]) && 
        (computerScreen.mouseY > mainMenuBox[1] && computerScreen.mouseY < mainMenuBox[1] + mainMenuBox[3])) {
        computerScreen.stroke(255);
        computerScreen.fill(#8E8B89);
        computerScreen.rect(mainMenuBox[0], mainMenuBox[1], mainMenuBox[2], mainMenuBox[3], mainMenuBox[4]);
        computerScreen.fill(255);
        computerScreen.text("Quit Training", mainMenuBox[0], mainMenuBox[1]+30, mainMenuBox[2], mainMenuBox[3]);
        computerScreen.noFill();
      }

      computerScreen.image(trainingGif, computerScreen.width/2 - 150, 250, 300, 300); //animation
    }
    else {
      computerScreen.textAlign(LEFT);

      if (lastBall.isPlayerTwo) {
        computerScreen.text("Result: Player 2 scored", computerScreen.width/2 - 605, 200, 680, 50);
        computerScreen.stroke(255);
        computerScreen.fill(#FA00FF);
      }
      else {
        computerScreen.text("Result: Player 1 scored", computerScreen.width/2 - 605, 200, computerScreen.width, 50);
        computerScreen.stroke(255);
        computerScreen.fill(#FFF300);
      }
      computerScreen.ellipse(computerScreen.width/2, 222, 30, 30);


      computerScreen.stroke(255);
      computerScreen.fill(255);
      computerScreen.noFill();
      drawButtons(continueModifyBox, continueModify);
    }
  }


  void onMouseClicked() {
    debugMouse();

    int[] mainMenuBox = { 
      computerScreen.width/2-200, computerScreen.height - 150, 400, 100, 7
    };

    int[][] continueModifyBox = { 
      {
        computerScreen.width/2 - 605, computerScreen.height - 150, 400, 100, 7
      }
      , 
      {
        computerScreen.width/2 + 205, computerScreen.height - 150, 400, 100, 7
      }
    };

    if (!isPoint) {
      if ((computerScreen.mouseX > mainMenuBox[0] && computerScreen.mouseX < mainMenuBox[0] + mainMenuBox[2]) && 
        (computerScreen.mouseY > mainMenuBox[1] && computerScreen.mouseY < mainMenuBox[1] + mainMenuBox[3])) {
        colorMode(RGB);
        background(0);
        computerScreen.background(0);
        modes[0] = new MainMenu();
        modes[3] = new Pattern();
        mode = MAIN_MENU;
      }
    }
    else {
      for (int i=0; i<2; i++) { // buttons click behaviors
        if ((computerScreen.mouseX > continueModifyBox[i][0] && computerScreen.mouseX < continueModifyBox[i][0] + continueModifyBox[i][2]) && 
          (computerScreen.mouseY > continueModifyBox[i][1] && computerScreen.mouseY < continueModifyBox[i][1] + continueModifyBox[i][3])) {
          if (i==0) { //quit button in case of more repetitions
            colorMode(RGB);
            destPosition = new PVector(0, 0);
            lastBall = null;
            isPoint = false;
            background(0);
            computerScreen.background(0);
            modes[0] = new MainMenu();
            modes[3] = new Pattern();
            mode = MAIN_MENU;
          }
          else {
            colorMode(RGB);
            background(0);
            computerScreen.background(0);
            modes[3] = new Pattern();
            return;
          }
        }
      }
    }
  }

  void updateBall(float x, float y) {
    destPosition = new PVector(x, y);
  }

  void onHit(Hit hit) {

    if (!isPoint) {
      Ball curBall = new Ball(hit.x, hit.y, hit.isRightSide, hit.tableWidth, hit.tableHeight);

      println("curBall x:"+curBall.getPixelVector().x+" y:"+curBall.getPixelVector().y+" isRightSide:"+ curBall.isRightSide);
      curBall.isServe=checkServe(curBall);
      curBall.isPlayerTwo=checkPlayerTwo(curBall);
      isDoubleHit = checkDoubleHit(curBall);

      training.add(curBall);

      println(" isServe:"+ curBall.isServe+" isPlayerTwo:"+ curBall.isPlayerTwo+" isTargetHit:"+curBall.isTargetHit+" isTargetError:"+curBall.isTargetError);
      lastBall = curBall;
    }
  }

  void showLastPoint() {
    PFont verdana12 = loadFont("Verdana-12.vlw");
    textFont(verdana12);

    nLines = training.size()-1;
    if (training.size()>0) {
      for (int i=1; i<training.size(); i++) {
        if (!interpoleWhiteFlag)
          interpole(training.get(i-1).getPixelVector(), training.get(i).getPixelVector(), i);
        else
          interpoleWhite(training.get(i-1).getPixelVector(), training.get(i).getPixelVector(), i);
        if (training.get(i-1).isPlayerTwo) {
          //stroke(#BC00B0);
          //fill(#BC00B0);
          fill(#FA00FF);
          stroke(255);
        }
        else {
          fill(#FFF300);
          stroke(255);
        }
        ellipse(training.get(i-1).getPixelVector().x, training.get(i-1).getPixelVector().y, 44, 44);
        stroke(255);
        fill(255);
        text(i, (training.get(i-1).getPixelVector().x), (training.get(i-1).getPixelVector().y)+5);
        if (training.get(i).isPlayerTwo) {
          //stroke(#BC00B0);
          //fill(#BC00B0);
          fill(#FA00FF);
          stroke(255);
        }
        else {
          fill(#FFF300);
          stroke(255);
        }
        if (training.get(i).isPoint)
          ellipse(training.get(i).getPixelVector().x, training.get(i).getPixelVector().y, 60, 60);
        else
          ellipse(training.get(i).getPixelVector().x, training.get(i).getPixelVector().y, 44, 44);
        stroke(255);
        fill(255);
        text(i+1, (training.get(i).getPixelVector().x), (training.get(i).getPixelVector().y)+5);
      }
    }
  }


  void interpole(PVector p1, PVector p2, int multiplier) {
    int index = 160 - (multiplier-1)*(160/nLines);
    float dis = dist(p1.x, p1.y, p2.x, p2.y);
    int n = int(dis);
    PVector diff = new PVector((p2.x-p1.x)/n, (p2.y-p1.y)/n);
    strokeWeight(5);
    colorMode(HSB);
    for (int i=1;i<n;i++) {
      try {
        stroke(index-(160/nLines*i/n), 255, 255);
      } 
      catch (Exception e) {
      }
      point(p1.x+diff.x*i, p1.y+diff.y*i);
    }
  }

  void interpoleWhite(PVector p1, PVector p2, int multiplier) {
    int index = 100 + (multiplier-1)*(155/nLines);
    float dis = dist(p1.x, p1.y, p2.x, p2.y);
    int n = int(dis);
    PVector diff = new PVector((p2.x-p1.x)/n, (p2.y-p1.y)/n);
    strokeWeight(5);
    for (int i=1;i<n;i++) {
      try {
        stroke(index+(155/nLines*i/n));
      } 
      catch (Exception e) {
      }
      point(p1.x+diff.x*i, p1.y+diff.y*i);
    }
  }

  void checkTimeout() { //checks if the last ball reached the timeout, which means that should be a point
    if (lastBall!=null && (millis()-lastBall.timestamp>TIMEOUT)) {
      if ((training.size()==1 && lastBall.isRightSide != playerOneIsRightSide) || (training.size()>1 && training.get(training.size()-2).isPoint == true && lastBall.isRightSide != playerOneIsRightSide))
        training.get(training.size()-1).isPlayerTwo = false;
      else if ((training.size()==1 && lastBall.isRightSide == playerOneIsRightSide) || (training.size()>1 && training.get(training.size()-2).isPoint == true && lastBall.isRightSide == playerOneIsRightSide))
        training.get(training.size()-1).isPlayerTwo = true;
      training.get(training.size()-1).isPoint = true;
      lastBall.isPoint = true;
      lastBall.isPlayerTwo = training.get(training.size()-1).isPlayerTwo;
      println("update: isPlayerTwo: "+training.get(training.size()-1).isPlayerTwo+" isPoint: "+training.get(training.size()-1).isPoint);
      isPoint = true;
    }
  }

  boolean checkServe(Ball curBall) { // checks if the strike performed is a service
    if (lastBall == null || lastBall.isPoint == true)
      return true;
    else if (lastBall.isServe == true && lastBall.isPoint == true)
      return true;
    else if (training.size()>=2 && training.get(training.size()-2).isServe == true && lastBall.isServe == true && curBall.isRightSide != lastBall.isRightSide)
      if (training.get(training.size()-2).isPoint)
        return true;
      else
        return false;
    else if (lastBall.isServe == true && curBall.isRightSide != lastBall.isRightSide)
      return true;
    return false;
  }

  boolean checkDoubleHit(Ball curBall) { //checks if the ball bounces twice in the same
    if (lastBall != null) {
      if (lastBall.isRightSide == curBall.isRightSide && !lastBall.isPoint) {
        if (playerOneIsRightSide == curBall.isRightSide) {
          curBall.isPlayerTwo = true;
        }
        else {
          curBall.isPlayerTwo = false;
        }
        curBall.isPoint = true;
        isPoint = true;
        println("double hit");
        return true;
      }
    }
    return false;
  }


  boolean checkPlayerTwo(Ball curBall) { // checks if the last hit is performed by the player two/the trainer.
    //    // In case of a double bounce on the same side, the function associate the ball to the same player because is anyways a scored point,
    //    // either if is a mistake responce of one player on his own side and if the ball bounces twice on the same side7

    if ((lastBall == null && curBall.isRightSide != playerOneIsRightSide) || (lastBall != null && lastBall.isPoint == true && curBall.isRightSide != playerOneIsRightSide))
      return true;
    else if ((lastBall == null && curBall.isRightSide == playerOneIsRightSide) || (lastBall != null && lastBall.isPoint == true && curBall.isRightSide == playerOneIsRightSide))
      return false;
    else if (training.size()>=2 && training.get(training.size()-2).isServe == true && lastBall.isServe == true && training.get(training.size()-2).isPoint == true && curBall.isRightSide != lastBall.isRightSide)
      if (lastBall.isPlayerTwo == false)
        return false;
      else
        return true;  
    else if (training.size()>=2 && training.get(training.size()-2).isServe == true && lastBall.isServe == true && curBall.isRightSide != lastBall.isRightSide)
      if (lastBall.isPlayerTwo == true)
        return false;
      else
        return true;
    else if (lastBall != null && lastBall.isServe == true && curBall.isRightSide != lastBall.isRightSide && lastBall.isPlayerTwo == true)
      return true;
    else if (lastBall != null && lastBall.isRightSide == playerOneIsRightSide && curBall.isRightSide == playerOneIsRightSide)
      return true;
    else if (lastBall != null && lastBall.isRightSide != playerOneIsRightSide && curBall.isRightSide != playerOneIsRightSide)
      return false;
    else if (lastBall != null && lastBall.isRightSide != curBall.isRightSide && curBall.isRightSide == playerOneIsRightSide)
      return true;
    else 
      return false;
  }

  void onKeyPressed() {
    if (key == 'w' && isPoint) {
      if (!interpoleWhiteFlag) {
        interpoleWhiteFlag = true;
      }
      else {
        interpoleWhiteFlag = false;
      }
      background(0);
      showLastPoint();
    }
  }
}

