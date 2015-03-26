import controlP5.*;
import gifAnimation.*;

class Target extends Mode {
  boolean targetSelected = false;
  boolean continueSetupFlag = false;
  boolean startTrainingFlag = false;
  boolean repetitionComplete = false;
  boolean trainingComplete = false;
  int targetDiameter = 10;
  int repetitions = 1;
  boolean traineeIsRightSide = false;
  int goalHits = 10;
  Hit target;
  Ball lastBall;
  int bright = 0;
  boolean getWhite = false;
  ControlP5 cp5, cp6;
  int step = 1;
  int currentRepetition = 0;
  ArrayList[] trainings;
  ArrayList<Ball> training;

  float[] deviations;
  int[] errors;
  int hitCount = 0;
  float meanDeviation = 0.0;
  int errorCount = 0;

  void display() {
  }

  void secondDisplay() {
    computerScreen.background(0);

    int[] mainMenuBox = { 
      computerScreen.width/2-200, computerScreen.height - 150, 400, 100, 7
    };
    PFont verdana60 = loadFont("Verdana-60.vlw");
    PFont verdana48 = loadFont("Verdana-48.vlw");

    computerScreen.fill(255);
    computerScreen.textAlign(CENTER);
    computerScreen.textFont(verdana60);
    computerScreen.text("Target Training - Step "+step+"/2", 0, 50, computerScreen.width, computerScreen.height);

    computerScreen.textFont(verdana48); //main menu button
    computerScreen.stroke(255);
    computerScreen.noFill();
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

    if (!continueSetupFlag) 
      targetSelection();
    else if (trainingComplete)
      trainingResume();
    else if (!startTrainingFlag && repetitionComplete)
      repetitionResume(currentRepetition);
    else if (startTrainingFlag)
      startTraining();
    else
      continueSetup();
  }

  void targetSelection() {
    step = 1;
    int[][] continueModifyBox = { 
      {
        computerScreen.width/2 - 605, computerScreen.height - 300, 400, 100, 7
      }
      , 
      {
        computerScreen.width/2 + 205, computerScreen.height - 300, 400, 100, 7
      }
    };
    String[] continueModify = { 
      "Modify Target", "Continue"
    };

    PFont verdana48 = loadFont("Verdana-48.vlw");
    stroke(255);
    strokeWeight(6);
    noFill();
    computerScreen.textFont(verdana48);
    computerScreen.text("Move the pointer on the table and select the Target", 0, 200, computerScreen.width, 50);
    computerScreen.textAlign(LEFT);
    computerScreen.text("Modify the Target dimension", computerScreen.width/2 - 605, 300, 680, 50);

    if (cp5 == null) {
      cp5 = new ControlP5(computerScreen);
      cp5.addTextfield("centimeters")
        .setPosition(computerScreen.width/2+95, 300)
          .setSize(150, 50)
            .setFont(verdana48)
              .setFocus(true)
                .setColor(color(255, 255, 255))
                  .setInputFilter(ControlP5.INTEGER)
                    .setValue(str(targetDiameter));
    }
    targetDiameter=int(cp5.get(Textfield.class, "centimeters").getText());

    if (!targetSelected) {
      if (bright==90) { // highlights the table during the selection
        getWhite = true;
      } 
      else if (bright == 0) {
        getWhite = false;
      }
      if (getWhite)
        bright -= 2;
      else
        bright += 2;
      background(bright);
      ellipse(mouseX, mouseY, targetDiameter*CM_TO_IN*screenMultiplier, targetDiameter*CM_TO_IN*screenMultiplier);
    }
    else {
      background(0);
      ellipse(target.getPixelVector().x, target.getPixelVector().y, targetDiameter*CM_TO_IN*screenMultiplier, targetDiameter*CM_TO_IN*screenMultiplier);

      drawButtons(continueModifyBox, continueModify);
    }
  }

  void onHit(Hit hit) {
    if (!repetitionComplete && !trainingComplete && currentRepetition<(repetitions) && startTrainingFlag) {
      Ball curBall = new Ball(hit.x, hit.y, hit.isRightSide, hit.tableWidth, hit.tableHeight);

      println("curBall x:"+curBall.getPixelVector().x+" y:"+curBall.getPixelVector().y+" isRightSide:"+ curBall.isRightSide);
      curBall.isServe=checkServe(curBall);
      curBall.isPlayerTwo=checkPlayerTwo(curBall);
      isScoredTarget(curBall);

      training.add(curBall);

      println(" isServe:"+ curBall.isServe+" isPlayerTwo:"+ curBall.isPlayerTwo+" isTargetHit:"+curBall.isTargetHit+" isTargetError:"+curBall.isTargetError);
      lastBall = curBall;
    }
  }

  void onMouseClicked() {
    debugMouse();

    int[] mainMenuBox = { 
      computerScreen.width/2-200, computerScreen.height - 150, 400, 100, 7
    };
    int[][] continueModifyBox = { 
      {
        computerScreen.width/2 - 605, computerScreen.height - 300, 400, 100, 7
      }
      , 
      {
        computerScreen.width/2 + 205, computerScreen.height - 300, 400, 100, 7
      }
    };

    if ((computerScreen.mouseX > mainMenuBox[0] && computerScreen.mouseX < mainMenuBox[0] + mainMenuBox[2]) && 
      (computerScreen.mouseY > mainMenuBox[1] && computerScreen.mouseY < mainMenuBox[1] + mainMenuBox[3])) {
      if (startTrainingFlag || repetitionComplete || trainingComplete) {
        colorMode(RGB);
      }
      else if (continueSetupFlag) {
        cp6.remove("hits");
        cp6.remove("repetitions");
        cp6 = null;
      }
      else {
        cp5.remove("centimeters");
        cp5 = null;
      }
      targetSelected = false;
      continueSetupFlag = false;
      repetitionComplete = false;
      startTrainingFlag = false;
      trainingComplete = false;
      background(0);
      computerScreen.background(0);
      modes[0] = new MainMenu();
      modes[1] = new Target();
      mode = MAIN_MENU;
    }
    if (repetitionComplete) {
      continueModifyBox[0][1] = computerScreen.height - 150;
      continueModifyBox[1][1] = computerScreen.height - 150;

      if (!trainingComplete) {
        for (int i=0; i<2; i++) { // buttons click behaviors
          if ((computerScreen.mouseX > continueModifyBox[i][0] && computerScreen.mouseX < continueModifyBox[i][0] + continueModifyBox[i][2]) && 
            (computerScreen.mouseY > continueModifyBox[i][1] && computerScreen.mouseY < continueModifyBox[i][1] + continueModifyBox[i][3])) {
            if (i==0) { //quit button in case of more repetitions
              targetSelected = false;
              continueSetupFlag = false;
              repetitionComplete = false;
              startTrainingFlag = false;
              colorMode(RGB);
              background(0);
              computerScreen.background(0);
              modes[0] = new MainMenu();
              modes[1] = new Target();
              mode = MAIN_MENU;
            }
            else {
              if (currentRepetition == repetitions-1) {
                colorMode(RGB);
                trainingComplete = true;
                hitCount = 0;
                meanDeviation = 0.0;
                errorCount = 0;
                computerScreen.background(0);
                background(0);
                trainingResume();
                return;
              }
              else {
                repetitionComplete = false;
                startTrainingFlag = true;
                colorMode(RGB);
                background(0);              
                computerScreen.background(0);
                hitCount = 0;
                meanDeviation = 0.0;
                errorCount = 0;
                lastBall = null;
                training = new ArrayList<Ball>();
                currentRepetition++;
                startTraining();
                return;
              }
            }
          }
        }
      }
    }
    if (targetSelected || continueSetupFlag) {
      for (int i=0; i<2; i++) { // highlights the buttons
        if ((computerScreen.mouseX > continueModifyBox[i][0] && computerScreen.mouseX < continueModifyBox[i][0] + continueModifyBox[i][2]) && 
          (computerScreen.mouseY > continueModifyBox[i][1] && computerScreen.mouseY < continueModifyBox[i][1] + continueModifyBox[i][3])) {
          if (i==0) {
            target = null;
            targetSelected = false;
            if (continueSetupFlag && !repetitionComplete) {
              cp6.remove("hits");
              cp6.remove("repetitions");
              cp6 = null;
            } 
            continueSetupFlag = false;
            repetitionComplete = false;
            secondDisplay();
            return;
          }
          else if (continueSetupFlag & !trainingComplete) {
            cp6.remove("hits");
            cp6.remove("repetitions");
            cp6 = null;

            trainings = new ArrayList[repetitions];
            training = new ArrayList<Ball>();

            traineeIsRightSide = !target.isRightSide;
            println("trainee is right side: "+traineeIsRightSide);
            deviations = new float[repetitions];
            errors = new int[repetitions];
            startTrainingFlag=true;
            startTraining();
            return;
          }
          else {
            cp5.remove("centimeters");
            cp5 = null;
            continueSetupFlag = true;
            secondDisplay();
            return;
          }
        }
      }
    }

    if (!targetSelected) {
      targetSelected = true;
      target = mouse2hit(mouseX, mouseY);
      return;
    }
  }

  void continueSetup() {
    step = 2;
    PFont verdana48 = loadFont("Verdana-48.vlw");

    int[][] continueModifyBox = { 
      {
        computerScreen.width/2 - 605, computerScreen.height - 300, 400, 100, 7
      }
      , 
      {
        computerScreen.width/2 + 205, computerScreen.height - 300, 400, 100, 7
      }
    };
    String[] continueModify = { 
      "Modify Target", "Start"
    };

    stroke(255);
    strokeWeight(4);
    noFill();
    computerScreen.textAlign(LEFT);
    computerScreen.textFont(verdana48);
    computerScreen.text("Number of hits on the target", computerScreen.width/2 - 605, 200, 680, 50);
    computerScreen.text("Number of repetitions", computerScreen.width/2 - 605, 300, 680, 50);

    if (cp6 == null) {
      cp6 = new ControlP5(computerScreen);
      cp6.addTextfield("hits")
        .setPosition(computerScreen.width/2+95, 200)
          .setSize(150, 50)
            .setFont(verdana48)
              .setFocus(true)
                .setColor(color(255, 255, 255))
                  .setInputFilter(ControlP5.INTEGER)
                    .setValue(str(goalHits));
      cp6.addTextfield("repetitions")
        .setPosition(computerScreen.width/2+95, 300)
          .setSize(150, 50)
            .setFont(verdana48)
              .setColor(color(255, 255, 255))
                .setInputFilter(ControlP5.INTEGER)
                  .setValue(str(repetitions));
    }
    goalHits=int(cp6.get(Textfield.class, "hits").getText());
    repetitions=int(cp6.get(Textfield.class, "repetitions").getText());

    drawButtons(continueModifyBox, continueModify);
  }

  void startTraining() {
    if (!repetitionComplete && !trainingComplete && currentRepetition<(repetitions)) {
      secondScreenTraining();
      tableTraining();
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

  boolean checkPlayerTwo(Ball curBall) { // checks if the last hit is performed by the player two/the trainer.
    //    // In case of a double bounce on the same side, the function associate the ball to the same player because is anyways a scored point,
    //    // either if is a mistake responce of one player on his own side and if the ball bounces twice on the same side7

    if ((lastBall == null && curBall.isRightSide != traineeIsRightSide) || (lastBall != null && lastBall.isPoint == true && curBall.isRightSide != traineeIsRightSide))
      return true;
    else if ((lastBall == null && curBall.isRightSide == traineeIsRightSide) || (lastBall != null && lastBall.isPoint == true && curBall.isRightSide == traineeIsRightSide))
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
    else if (lastBall != null && lastBall.isRightSide == traineeIsRightSide && curBall.isRightSide == traineeIsRightSide)
      return true;
    else if (lastBall != null && lastBall.isRightSide != traineeIsRightSide && curBall.isRightSide != traineeIsRightSide)
      return false;
    else if (lastBall != null && lastBall.isRightSide != curBall.isRightSide && curBall.isRightSide == traineeIsRightSide)
      return true;
    else 
      return false;
  }

  void checkTimeout() { //checks if the last ball reached the timeout, which means that should be a point
    if (lastBall!=null && (millis()-lastBall.timestamp>TIMEOUT)) {
      if ((training.size()==1 && lastBall.isRightSide != traineeIsRightSide) || (training.size()>1 && training.get(training.size()-2).isPoint == true && lastBall.isRightSide != traineeIsRightSide))
        training.get(training.size()-1).isPlayerTwo = false;
      else if ((training.size()==1 && lastBall.isRightSide == traineeIsRightSide) || (training.size()>1 && training.get(training.size()-2).isPoint == true && lastBall.isRightSide == traineeIsRightSide))
        training.get(training.size()-1).isPlayerTwo = true;
      training.get(training.size()-1).isPoint = true;
      lastBall.isPoint = true;
      lastBall.isPlayerTwo = training.get(training.size()-1).isPlayerTwo;
      println("update: isPlayerTwo: "+training.get(training.size()-1).isPlayerTwo+" isPoint: "+training.get(training.size()-1).isPoint);
    }
  }

  void isScoredTarget(Ball curBall) { // checks if the target has been hit by the ball
    if (curBall.isPlayerTwo || curBall.isServe)
      return;
    if ((curBall.isRightSide == target.isRightSide && 
      dist(curBall.x, curBall.y, target.x, target.y) <= targetDiameter / 2*CM_TO_IN) &&
      curBall.isPlayerTwo == false && curBall.isServe == false)
    {
      hitCount++;
      curBall.isTargetHit = true;
      curBall.isTargetError = false;
    }
    else if ((curBall.isRightSide == target.isRightSide && 
      dist(curBall.x, curBall.y, target.x, target.y) > targetDiameter/2*CM_TO_IN) &&
      curBall.isPlayerTwo == false && curBall.isServe == false) {
      curBall.isTargetHit = false;
      curBall.isTargetError = true;
      errorCount++;
      meanDeviation += dist(curBall.x, curBall.y, target.x, target.y)/CM_TO_IN;
    }
    else {
      curBall.isTargetHit = false;
      curBall.isTargetError = false;
    }
  }

  void secondScreenTraining() {
    int[] mainMenuBox = { 
      computerScreen.width/2-200, computerScreen.height - 150, 400, 100, 7
    };

    PFont verdana60 = loadFont("Verdana-60.vlw");
    PFont verdana48 = loadFont("Verdana-48.vlw");

    computerScreen.background(0);

    computerScreen.fill(255);
    computerScreen.textAlign(CENTER);
    computerScreen.textFont(verdana60);
    computerScreen.text("Target Training - Exercise "+(currentRepetition+1)+"/"+repetitions, 0, 50, computerScreen.width, computerScreen.height);

    computerScreen.textFont(verdana48);
    computerScreen.text("Number of target's hits: "+hitCount+"/"+goalHits, 0, 200, computerScreen.width, 50);

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

  void tableTraining() {
    //debug = true;
    PFont verdana22 = loadFont("Verdana-22.vlw");
    textAlign(LEFT);
    textFont(verdana22);
    noFill();
    stroke(255);
    strokeWeight(6);
    if (hitCount <= goalHits) {
      ellipse (target.getPixelVector().x, target.getPixelVector().y, targetDiameter*CM_TO_IN*screenMultiplier, targetDiameter*CM_TO_IN*screenMultiplier);
      for (int i=0; i<training.size(); i++) {
        if (training.get(i).isTargetHit) {
          noFill();
          stroke(255);
          strokeWeight(2);
          ellipse (training.get(i).getPixelVector().x, training.get(i).getPixelVector().y, 44, 44);
        }
      }
      if (hitCount == goalHits) {
        //debug = false;

        repetitionComplete = true;
        startTrainingFlag = false;
        trainings[currentRepetition] = training;
        deviations[currentRepetition] = meanDeviation;
        errors[currentRepetition] = errorCount;
        repetitionResume(currentRepetition);
        tableResume(currentRepetition);
      }
    }
    checkTimeout();
  }

  void repetitionResume(int repetition) {
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
    computerScreen.text("Target Training - Exercise "+(repetition+1)+"/"+repetitions, 0, 50, computerScreen.width, computerScreen.height);

    computerScreen.textFont(verdana48);
    computerScreen.textAlign(LEFT);
    computerScreen.text("Number of Errors: "+errors[repetition]+"/"+(goalHits+errors[repetition]), computerScreen.width/2 - 605, 200, computerScreen.width, 50);
    if (errors[repetition] == 0) {
      computerScreen.text("Mean Deviation: 0.0 cm", computerScreen.width/2 - 605, 300, 680, 50);
    }
    else {
      computerScreen.text("Mean Deviation: "+(deviations[repetition]/errors[repetition])+ " cm", computerScreen.width/2 - 605, 300, computerScreen.width, 50);
    }
    computerScreen.noFill();

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
  void tableResume(int repetition) { //colors the target depending on the percentage of the errors
    background(0);
    colorMode(HSB);
    int[] colors = { 
      80, 50, 20, 0
    };
    int col = 0;
    println(goalHits+"/"+(goalHits+errors[repetition])+" ="+goalHits/(goalHits+errors[repetition]));

    int percentage = int(float(goalHits)/float((goalHits+errors[repetition]))*100.0);

    for (int i=0; i<training.size(); i++) {
      if (training.get(i).isTargetError) {
        noFill();
        stroke(255);
        strokeWeight(2);
        ellipse (training.get(i).getPixelVector().x, training.get(i).getPixelVector().y, 44, 44);
      }
    }
    if (percentage >= 75)
      col = colors[0];
    else if (percentage >= 50)
      col = colors[1];
    else if (percentage >= 25)
      col = colors[2];
    else
      col = colors[3];
    fill(col, 255, 255);
    stroke(255);   
    strokeWeight(6);
    ellipse (target.getPixelVector().x, target.getPixelVector().y, targetDiameter*CM_TO_IN*screenMultiplier, targetDiameter*CM_TO_IN*screenMultiplier);
    fill(255);
    textAlign(LEFT);
    text(percentage + "%", target.getPixelVector().x-23, target.getPixelVector().y+8);
  }

  void trainingResume() {
    int[] mainMenuBox = { 
      computerScreen.width/2-200, computerScreen.height - 150, 400, 100, 7
    };
    int totError = 0; 
    float totMeanDeviation = 0.0;
    for (int i=0; i<repetitions; i++) {
      totError+=errors[i];
      totMeanDeviation += deviations[i];
    }
    PFont verdana60 = loadFont("Verdana-60.vlw");
    PFont verdana48 = loadFont("Verdana-48.vlw");

    computerScreen.background(0);

    computerScreen.fill(255);
    computerScreen.textAlign(CENTER);
    computerScreen.textFont(verdana60);
    computerScreen.text("Target Training - Overall Statistics", 0, 50, computerScreen.width, computerScreen.height);

    computerScreen.textFont(verdana48);
    computerScreen.textAlign(LEFT);

    computerScreen.text("Total Number of Errors: "+totError+"/"+((goalHits*repetitions)+totError), computerScreen.width/2 - 605, 200, computerScreen.width, 50);
    if (totError == 0) {
      computerScreen.text("Average Mean Deviation: 0.0 cm", computerScreen.width/2 - 605, 300, computerScreen.width, 50);
    }
    else {
      computerScreen.text("Average Mean Deviation: "+(totMeanDeviation/totError)+ " cm", computerScreen.width/2 - 605, 300, computerScreen.width, 50);
    }

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
    background(0);
    colorMode(HSB);
    int[] colors = { 
      80, 50, 20, 0
    };
    int col = 0;
    int percentage = int(float(goalHits*repetitions)/float((goalHits*repetitions)+totError)*100.0);

    for (int x=0; x<repetitions; x++) {
      training = trainings[x];
      for (int i=0; i<training.size(); i++) {
        if (training.get(i).isTargetError) {
          noFill();
          stroke(255);
          strokeWeight(2);
          ellipse (training.get(i).getPixelVector().x, training.get(i).getPixelVector().y, 44, 44);
        }
      }
    }
    if (percentage >= 75)
      col = colors[0];
    else if (percentage >= 50)
      col = colors[1];
    else if (percentage >= 25)
      col = colors[2];
    else
      col = colors[3];
    fill(col, 255, 255);  
    stroke(255);   
    strokeWeight(6); 
    ellipse (target.getPixelVector().x, target.getPixelVector().y, targetDiameter*CM_TO_IN*screenMultiplier, targetDiameter*CM_TO_IN*screenMultiplier);
    fill(255);
    textAlign(LEFT);
    text(percentage + "%", target.getPixelVector().x-23, target.getPixelVector().y+8);
  }
}

