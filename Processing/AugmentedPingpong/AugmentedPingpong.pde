import java.io.*;

DataThread ping_thread;
//String PYTHON         = "C:\\Python26";
String PYTHON_SCRIPT  = "\"D:\\Dropbox\\__Interactive\\Python\\training.py\"";

void setup() {
  size(200, 200);
  
  ping_thread = new DataThread();
  ping_thread.start();
}

void draw() { 
  // draw() must be present for mousePressed() to work
}

void mousePressed() {
  println("Python Training");
  //open("D:\\Dropbox\\__Interactive\\Augmented Table Tennis\\AugmentedTable 0.3\\Python\\training.py");
  //open("D:\\Dropbox\\__Interactive\\Augmented Table Tennis\\AugmentedTable 0.3\\Python\\hitdata-left.txt");
  //open("C:\\Program Files (x86)\\Adobe\\Adobe Photoshop CS3\\Photoshop.exe");
}

public class DataThread extends Thread {
  private boolean running;
  private boolean fresh;     // Is there fresh data to be polled?
  int[] labjack_fields = new int[16];
  
  // Constructor, create the thread
  // It is not running by default
  public DataThread() {
    running = false;
  }
  
  public void start() {
    // Set running equal to true
    running = true;
    fresh = false;
    // Print messages
    System.out.println("Starting data thread...");
    // Do whatever start does in Thread, don't forget this!
    super.start();
  }
  
  public void run () {
    try {
      String line;
      OutputStream stdin = null;
        
      Process p = Runtime.getRuntime().exec("notepad");
         
      BufferedReader input = new BufferedReader(new InputStreamReader(p.getInputStream()));
    
      while ((line = input.readLine()) != null) {
        String[] m = split(line, " ");
        labjack_fields[int(m[0])] = int(m[1]);
        Thread.currentThread().sleep(1); //Mysteriously Important Sleep Line
      }
    } catch(Exception err) {
      err.printStackTrace();
    }
  }
  
  public int getLatest(int index) {
    return labjack_fields[index];
  }
}
