import controlP5.*;
import gifAnimation.*;

class Service extends Mode {
  int repetitions;
  boolean repetitionsSelected;
  boolean repetitionComplete;
  boolean trainingComplete;
  ArrayList[] trainings;
  ArrayList<Ball> training;
  ControlP5 cp5;
  int currentRepetition;
  PFont verdana12, verdana36;

  Service() {
    repetitions = 1;
    currentRepetition = 0;
    repetitionsSelected = false;
    trainingComplete = false;
    repetitionComplete = false;
    verdana12 = loadFont("Verdana-12.vlw");
    verdana36 = loadFont("Verdana-36.vlw");
  }

  void display() {
    if (!trainingComplete && currentRepetition<(repetitions) && repetitionsSelected) {
      //debug=true;
      drawBallOnTable();
      if (!repetitionComplete)
        checkTimeout();
    }
    else
      debug=false;
  }

  void secondDisplay() {
    computerScreen.background(0);

    if (trainingComplete && repetitions>1) {
      trainingCompleted();
      return;
    }
    if (!repetitionsSelected) {
      setupTraining();
      return;
    }
    else if (!repetitionComplete) {
      startTraining();
      return;
    }
    else {
      trainingResume();
      return;
    }
  }
  void onHit(Hit hit) {
    if (!repetitionComplete && !trainingComplete && currentRepetition<(repetitions) && repetitionsSelected) {
      Ball curBall = new Ball(hit.x, hit.y, hit.isRightSide, 60, 54);

      println("curBall x:"+curBall.getPixelVector().x+" y:"+curBall.getPixelVector().y+" isRightSide:"+ curBall.isRightSide);
      training.add(curBall);
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

    int[][] previousNextBox = { 
      {
        computerScreen.width/2 - 605, computerScreen.height/2 - 50, 100, 100, 7
      }
      , 
      {
        computerScreen.width/2 + 505, computerScreen.height/2 - 50, 100, 100, 7
      }
    };

    if (!repetitionsSelected) {
      for (int i=0; i<2; i++) { // buttons click behaviors
        if ((computerScreen.mouseX > continueModifyBox[i][0] && computerScreen.mouseX < continueModifyBox[i][0] + continueModifyBox[i][2]) && 
          (computerScreen.mouseY > continueModifyBox[i][1] && computerScreen.mouseY < continueModifyBox[i][1] + continueModifyBox[i][3])) {
          if (i==0) { //quit button in case of more repetitions
            repetitionsSelected = false;
            trainingComplete = false;
            repetitionComplete = false;
            if (cp5 != null) {
              cp5.remove("repetitions");
              cp5 = null;
            }
            colorMode(RGB);
            background(0);
            computerScreen.background(0);
            modes[0] = new MainMenu();
            modes[2] = new Service();
            mode = MAIN_MENU;
          }
          else {
            repetitionsSelected = true;
            colorMode(RGB);
            cp5.remove("repetitions");
            cp5 = null;
            background(0);              
            computerScreen.background(0);
            training = new ArrayList<Ball>();
            trainings = new ArrayList[repetitions];
            startTraining();
            return;
          }
        }
      }
    }
    else if (!repetitionComplete) {
      if ((computerScreen.mouseX > mainMenuBox[0] && computerScreen.mouseX < mainMenuBox[0] + mainMenuBox[2]) && 
        (computerScreen.mouseY > mainMenuBox[1] && computerScreen.mouseY < mainMenuBox[1] + mainMenuBox[3])) {
        repetitionsSelected = false;
        trainingComplete = false;
        repetitionComplete = false;
        if (cp5 != null) {
          cp5.remove("repetitions");
          cp5 = null;
        }
        colorMode(RGB);
        background(0);
        computerScreen.background(0);
        modes[0] = new MainMenu();
        modes[2] = new Service();
        mode = MAIN_MENU;
      }
    }
    else if (!trainingComplete || (trainingComplete && repetitions == 1)) {
      if (repetitions == 1) {
        if ((computerScreen.mouseX > mainMenuBox[0] && computerScreen.mouseX < mainMenuBox[0] + mainMenuBox[2]) && 
          (computerScreen.mouseY > mainMenuBox[1] && computerScreen.mouseY < mainMenuBox[1] + mainMenuBox[3])) {
          repetitionsSelected = false;
          trainingComplete = false;
          repetitionComplete = false;
          if (cp5 != null) {
            cp5.remove("repetitions");
            cp5 = null;
          }
          colorMode(RGB);
          background(0);
          computerScreen.background(0);
          modes[0] = new MainMenu();
          modes[2] = new Service();
          mode = MAIN_MENU;
        }
      }
      else {
        for (int i=0; i<2; i++) { // buttons click behaviors
          if ((computerScreen.mouseX > continueModifyBox[i][0] && computerScreen.mouseX < continueModifyBox[i][0] + continueModifyBox[i][2]) && 
            (computerScreen.mouseY > continueModifyBox[i][1] && computerScreen.mouseY < continueModifyBox[i][1] + continueModifyBox[i][3])) {
            if (i==0) { //quit button in case of more repetitions
              repetitionsSelected = false;
              trainingComplete = false;
              repetitionComplete = false;
              if (cp5 != null) {
                cp5.remove("repetitions");
                cp5 = null;
              }
              colorMode(RGB);
              background(0);
              computerScreen.background(0);
              modes[0] = new MainMenu();
              modes[2] = new Service();
              mode = MAIN_MENU;
            }
            else {
              if (currentRepetition<repetitions-1) {
                repetitionsSelected = true;
                repetitionComplete = false;
                trainings[currentRepetition] = training;
                training = new ArrayList<Ball>();
                currentRepetition++;
                colorMode(RGB);
                background(0);              
                computerScreen.background(0);
                startTraining();
                return;
              }
              else {
                trainingComplete = true;
                trainings[currentRepetition] = training;
                colorMode(RGB);
                background(0);              
                computerScreen.background(0);
                currentRepetition = 0;
                training = trainings[currentRepetition];
                trainingCompleted();
                return;
              }
            }
          }
        }
      }
    }
    else {
      if ((computerScreen.mouseX > mainMenuBox[0] && computerScreen.mouseX < mainMenuBox[0] + mainMenuBox[2]) && 
        (computerScreen.mouseY > mainMenuBox[1] && computerScreen.mouseY < mainMenuBox[1] + mainMenuBox[3])) {
        repetitionsSelected = false;
        trainingComplete = false;
        repetitionComplete = false;
        if (cp5 != null) {
          cp5.remove("repetitions");
          cp5 = null;
        }
        colorMode(RGB);
        background(0);
        computerScreen.background(0);
        modes[0] = new MainMenu();
        modes[2] = new Service();
        mode = MAIN_MENU;
      }
      for (int i=0; i<2; i++) { // buttons click behaviors
        if ((computerScreen.mouseX > previousNextBox[i][0] && computerScreen.mouseX < previousNextBox[i][0] + previousNextBox[i][2]) && 
          (computerScreen.mouseY > previousNextBox[i][1] && computerScreen.mouseY < previousNextBox[i][1] + previousNextBox[i][3])) {
          if (i==0) {
            currentRepetition--;
            if (currentRepetition == -1)
              currentRepetition = repetitions-1;
          }
          else {
            currentRepetition++;
            if (currentRepetition == repetitions)
              currentRepetition = 0;
          }
          training = trainings[currentRepetition];
          trainingCompleted();
        }
      }
    }
  }

  void setupTraining() {
    PFont verdana60 = loadFont("Verdana-60.vlw");

    computerScreen.fill(255);
    computerScreen.textAlign(CENTER);
    computerScreen.textFont(verdana60);
    computerScreen.text("Service Training", 0, 50, computerScreen.width, computerScreen.height);

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
      "Main Menu", "Continue"
    };

    PFont verdana48 = loadFont("Verdana-48.vlw");
    computerScreen.textFont(verdana48);

    computerScreen.textAlign(LEFT);
    computerScreen.text("Number of repetitions", computerScreen.width/2 - 605, 200, 680, 50);

    if (cp5 == null) {
      cp5 = new ControlP5(computerScreen);
      cp5.addTextfield("repetitions")
        .setPosition(computerScreen.width/2+95, 200)
          .setSize(150, 50)
            .setFont(verdana48)
              .setFocus(true)
                .setColor(color(255, 255, 255))
                  .setInputFilter(ControlP5.INTEGER)
                    .setValue(str(repetitions));
    }
    repetitions=int(cp5.get(Textfield.class, "repetitions").getText());
    computerScreen.noFill();

    drawButtons(continueModifyBox, continueModify);
  }

  void startTraining() {
    int[] mainMenuBox = { 
      computerScreen.width/2-200, computerScreen.height - 150, 400, 100, 7
    };

    PFont verdana60 = loadFont("Verdana-60.vlw");
    PFont verdana48 = loadFont("Verdana-48.vlw");

    computerScreen.fill(255);
    computerScreen.textAlign(CENTER);
    computerScreen.textFont(verdana60);
    computerScreen.text("Target Training - Exercise "+(currentRepetition+1)+"/"+repetitions, 0, 50, computerScreen.width, computerScreen.height);

    computerScreen.textFont(verdana48);
    computerScreen.text("Play a Service", 0, 200, computerScreen.width, 50);
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

  void drawBallOnTable() {
    textFont(verdana12);
    stroke(255);
    noFill();
    for (int i=0; training.size()>0 && i<training.size(); i++) {
      ellipse(training.get(i).getPixelVector().x, training.get(i).getPixelVector().y, 44, 44);
      text(i+1, (training.get(i).getPixelVector().x), (training.get(i).getPixelVector().y)+5);
    }
  }

  void trainingResume() {
    int diff;
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
      "Quit Training", "Start Next"
    };
    if (currentRepetition == repetitions-1)
      continueModify[1] = "Summary";

    PFont verdana60 = loadFont("Verdana-60.vlw");
    PFont verdana48 = loadFont("Verdana-48.vlw");

    computerScreen.background(0);

    computerScreen.fill(255);
    computerScreen.textAlign(CENTER);
    computerScreen.textFont(verdana60);
    computerScreen.text("Target Training - Exercise "+(currentRepetition+1)+"/"+repetitions, 0, 50, computerScreen.width, computerScreen.height);

    computerScreen.textFont(verdana48);
    computerScreen.textAlign(LEFT);

    computerScreen.noFill();
    computerScreen.stroke(255);

    for (int i=0; training.size()>0 && i<training.size(); i++) {
      computerScreen.ellipse(computerScreen.width/2 - 55, 170 + (i*88), 44, 44);
      computerScreen.textFont(verdana12);
      computerScreen.text(i+1, computerScreen.width/2 - 58, 170 + (i*88) +5);
      if (i+1<training.size()) {
        diff = training.get(i+1).timestamp - training.get(i).timestamp;
        computerScreen.line(computerScreen.width/2 - 55, 192 + (i*88), computerScreen.width/2 - 55, 236 + (i*88));
        computerScreen.textFont(verdana36);
        computerScreen.text(diff+" ms", computerScreen.width/2 - 2, 236 + (i*88)-7);
        computerScreen.textFont(verdana12);
        computerScreen.ellipse(computerScreen.width/2 - 55, 170 + ((i+1)*88), 44, 44);
        computerScreen.text(i+2, computerScreen.width/2 - 58, 170 + ((i+1)*88) +5);
      }
    }


    computerScreen.textFont(verdana48);

    if (repetitions == 1) {
      trainingComplete = true;

      computerScreen.stroke(255); //single main menu button if the exercise is carried out only once
      computerScreen.noFill();
      computerScreen.textAlign(CENTER);

      computerScreen.rect(mainMenuBox[0], mainMenuBox[1], mainMenuBox[2], mainMenuBox[3], mainMenuBox[4]);
      computerScreen.text("Main Menu", mainMenuBox[0], mainMenuBox[1]+30, mainMenuBox[2], mainMenuBox[3]);
      if ((computerScreen.mouseX > mainMenuBox[0] && computerScreen.mouseX < mainMenuBox[0] + mainMenuBox[2]) && 
        (computerScreen.mouseY > mainMenuBox[1] && computerScreen.mouseY < mainMenuBox[1] + mainMenuBox[3])) {
        computerScreen.stroke(255);
        computerScreen.fill(#8E8B89);
        computerScreen.rect(mainMenuBox[0], mainMenuBox[1], mainMenuBox[2], mainMenuBox[3], mainMenuBox[4]);
        computerScreen.fill(255);
        computerScreen.text("Main Menu", mainMenuBox[0], mainMenuBox[1]+30, mainMenuBox[2], mainMenuBox[3]);
        computerScreen.noFill();
      }
    }
    else { //draw quit training and start new repetition buttons
      drawButtons(continueModifyBox, continueModify);
    }
  }

  void checkTimeout() { //checks if the last ball reached the timeout, which means that should be a point
    if (training.size()>0 && (millis()-training.get(training.size()-1).timestamp>TIMEOUT)) {
      repetitionComplete = true;
    }
  }

  void trainingCompleted() {
    int diff;
    int[] mainMenuBox = { 
      computerScreen.width/2-200, computerScreen.height - 150, 400, 100, 7
    };

    int[][] previousNextBox = { 
      {
        computerScreen.width/2 - 605, computerScreen.height/2 - 50, 100, 100, 7
      }
      , 
      {
        computerScreen.width/2 + 505, computerScreen.height/2 - 50, 100, 100, 7
      }
    };

    String[] previousNext = { 
      "<<", ">>"
    };

    PFont verdana60 = loadFont("Verdana-60.vlw");
    PFont verdana48 = loadFont("Verdana-48.vlw");

    computerScreen.background(0);
    background(0);

    computerScreen.fill(255);
    computerScreen.textAlign(CENTER);
    computerScreen.textFont(verdana60);
    computerScreen.text("Target Training - Summary: Exercise "+(currentRepetition+1)+"/"+repetitions, 0, 50, computerScreen.width, computerScreen.height);

    computerScreen.textFont(verdana48);
    computerScreen.textAlign(LEFT);

    computerScreen.noFill();
    computerScreen.stroke(255);

    for (int i=0; training.size()>0 && i<training.size(); i++) {
      computerScreen.ellipse(computerScreen.width/2 - 55, 170 + (i*88), 44, 44);
      computerScreen.textFont(verdana12);
      computerScreen.text(i+1, computerScreen.width/2 - 58, 170 + (i*88) +5);

      ellipse(training.get(i).getPixelVector().x, training.get(i).getPixelVector().y, 44, 44);
      text(i+1, (training.get(i).getPixelVector().x), (training.get(i).getPixelVector().y)+5);

      if (i+1<training.size()) {
        diff = training.get(i+1).timestamp - training.get(i).timestamp;
        computerScreen.line(computerScreen.width/2 - 55, 192 + (i*88), computerScreen.width/2 - 55, 236 + (i*88));
        computerScreen.textFont(verdana36);
        computerScreen.text(diff+" ms", computerScreen.width/2 - 2, 236 + (i*88)-7);
        computerScreen.textFont(verdana12);
        computerScreen.ellipse(computerScreen.width/2 - 55, 170 + ((i+1)*88), 44, 44);
        computerScreen.text(i+2, computerScreen.width/2 - 58, 170 + ((i+1)*88) +5);
      }
    }


    computerScreen.textFont(verdana48);

    computerScreen.stroke(255); //single main menu button if the exercise is carried out only once
    computerScreen.noFill();
    computerScreen.textAlign(CENTER);

    computerScreen.rect(mainMenuBox[0], mainMenuBox[1], mainMenuBox[2], mainMenuBox[3], mainMenuBox[4]);
    computerScreen.text("Main Menu", mainMenuBox[0], mainMenuBox[1]+30, mainMenuBox[2], mainMenuBox[3]);
    if ((computerScreen.mouseX > mainMenuBox[0] && computerScreen.mouseX < mainMenuBox[0] + mainMenuBox[2]) && 
      (computerScreen.mouseY > mainMenuBox[1] && computerScreen.mouseY < mainMenuBox[1] + mainMenuBox[3])) {
      computerScreen.stroke(255);
      computerScreen.fill(#8E8B89);
      computerScreen.rect(mainMenuBox[0], mainMenuBox[1], mainMenuBox[2], mainMenuBox[3], mainMenuBox[4]);
      computerScreen.fill(255);
      computerScreen.text("Main Menu", mainMenuBox[0], mainMenuBox[1]+30, mainMenuBox[2], mainMenuBox[3]);
      computerScreen.noFill();
    }

    drawButtons(previousNextBox, previousNext);
  }
}

