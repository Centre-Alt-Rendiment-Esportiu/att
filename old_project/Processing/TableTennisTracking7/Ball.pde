class Ball extends Hit{
  int timestamp;
  boolean isPlayerTwo;
  boolean isServe;
  boolean isPoint;
  boolean isTargetHit;
  boolean isTargetError;
  
  Ball(float x, float y, boolean isRightSide, int tableWidth, int tableHeight, boolean isPlayerTwo, boolean isServe, boolean isTargetHit, boolean isTargetError){
    super(x, y, isRightSide, tableWidth, tableHeight);
    this.timestamp = millis();
    this.isServe = isServe;
    this.isPoint = false;
    this.isPlayerTwo = isPlayerTwo;
    this.isTargetHit = isTargetHit;
    this.isTargetError = isTargetError;
  }
  
  Ball(float x, float y, boolean isRightSide, int tableWidth, int tableHeight){
    super(x, y, isRightSide, tableWidth, tableHeight);
    this.timestamp = millis();
    this.isServe = false;
    this.isPoint = false;
    this.isPlayerTwo = false;
    this.isTargetHit = false;
    this.isTargetError = false;
  }
}
