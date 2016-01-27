class MainMenu extends Mode {
  String[] options = new String[3];
  int[][] optionsRects;

  MainMenu() {
    options[0] = "Target Training";
    options[1] = "Service Training";
    options[2] = "Point's Pattern";
  }

  void display() {
    background(0);
    color c = #FFFFFF;
    fill(c);
    PFont verdana100;
    verdana100 = loadFont("Verdana-100.vlw");
    textAlign(CENTER);
    textFont(verdana100);
    text("Table Tennis Tracking", 0, height/2 - 100, width, height);
  }

  void secondDisplay() {
    colorMode(RGB);

    int[][] optionsRects = { 
      {
        computerScreen.width/2-200, 150, 400, 100, 7
      }
      , 
      {
        computerScreen.width/2-200, 320, 400, 100, 7
      }
      , 
      {
        computerScreen.width/2-200, 490, 400, 100, 7
      }
    };

    computerScreen.background(0);
    computerScreen.fill(255);
    PFont verdana60 = loadFont("Verdana-60.vlw");
    PFont verdana48 = loadFont("Verdana-48.vlw");

    computerScreen.textAlign(CENTER);
    computerScreen.textFont(verdana60);
    computerScreen.text("Select the Training", 0, 50, computerScreen.width, computerScreen.height);

    computerScreen.textFont(verdana48);
    computerScreen.stroke(255);
    computerScreen.noFill();
    for (int i=0; i<3; i++) {
      computerScreen.rect(optionsRects[i][0], optionsRects[i][1], optionsRects[i][2], optionsRects[i][3], optionsRects[i][4]);
      computerScreen.text(options[i], optionsRects[i][0], optionsRects[i][1]+30, optionsRects[i][2], optionsRects[i][3]);
    }
    for (int i=0; i<3; i++) { // highlights the buttons
      if ((computerScreen.mouseX > optionsRects[i][0] && computerScreen.mouseX < optionsRects[i][0] + optionsRects[i][2]) && 
        (computerScreen.mouseY > optionsRects[i][1] && computerScreen.mouseY < optionsRects[i][1] + optionsRects[i][3])) {
        computerScreen.stroke(255);
        computerScreen.fill(#8E8B89);
        computerScreen.rect(optionsRects[i][0], optionsRects[i][1], optionsRects[i][2], optionsRects[i][3], optionsRects[i][4]);
        computerScreen.fill(255);
        computerScreen.text(options[i], optionsRects[i][0], optionsRects[i][1]+30, optionsRects[i][2], optionsRects[i][3]);
      }
    }
  }

  void chooseOption(int index) {
    mode = index;
    background(0);
    computerScreen.background(0);
  }

  void onHit(Hit hit) {
  }

  void onMouseClicked() {
    int[][] optionsRects = { 
      {
        computerScreen.width/2-200, 150, 400, 150, 7
      }
      , 
      {
        computerScreen.width/2-200, 320, 400, 150, 7
      }
      , 
      {
        computerScreen.width/2-200, 490, 400, 150, 7
      }
    };
    for (int i=0; i<3; i++) { // checks what is the selected menu item and loads the relative screen
      if ((computerScreen.mouseX > optionsRects[i][0] && computerScreen.mouseX < optionsRects[i][0] + optionsRects[i][2]) && 
        (computerScreen.mouseY > optionsRects[i][1] && computerScreen.mouseY < optionsRects[i][1] + optionsRects[i][3])) {
        chooseOption(i+1);
      }
    }
  }
}

