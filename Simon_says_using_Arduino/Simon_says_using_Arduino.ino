#include <Entropy.h>  //Random number generation library
String str = "";
String question = "";
String your_answer = "";
String game_mode = "";
int a, score = 0;
int n = 1, j = 0, i;
int simon_q[50] = {}, simon_a[50] = {};
int ans_delay = 200;
int q_delay;
int flag;
char apple[15];
char strin[15];
char ansin[5];

void setup() {
  pinMode(2, OUTPUT);    //Red LED
  pinMode(3, OUTPUT);    //Green LED
  pinMode(4, OUTPUT);    //Blue LED
  Serial.begin(9600);    //Begin serial communication
  Entropy.Initialize();  //Initialize random number generation

  Serial.println("Select Difficulty:\neasy\nnormal\nhard\ndynamic");  //Select game mode
  while (game_mode == "")                                             //Wait for input
  {
    Entropy.random(2, 5);  //Randomize number in background
    game_mode = Serial.readString();
  }
  game_mode.toCharArray(apple, 10);
  if (strcmp(apple, "easy") == 10) {
    Serial.println("game mode = easy");
    q_delay = 500;
  } else if (strcmp(apple, "normal") == 10) {
    Serial.println("game mode = normal");
    q_delay = 300;
  } else if (strcmp(apple, "hard") == 10) {
    Serial.println("game mode = hard");
    q_delay = 100;
  } else if (strcmp(apple, "im") == 10) {
    Serial.println("game mode = hard");
    q_delay = 0;
  } else if (strcmp(apple, "dynamic") == 10) {
    Serial.println("game mode = dynamic");
    q_delay = 500;
  } else {
    game_mode == "";
  }  //Reset for invalid input

  Serial.println("Type 'start' to play");
}
void loop() {

  while (str == "")  //Wait for "start" input
  {
    Entropy.random(2, 5);
    str = Serial.readString();
    str.toCharArray(strin, 10);
  }
  if (strcmp(strin, "start") == 10 || strcmp(strin, "start") == 0) {  //On input blink all LEDS to indicate start of game
    digitalWrite(2, HIGH);
    digitalWrite(3, HIGH);
    digitalWrite(4, HIGH);
    delay(750);
    digitalWrite(2, LOW);
    digitalWrite(3, LOW);
    digitalWrite(4, LOW);
    delay(750);

    for (i = 0; i < n; i++)  //Generate a random pattern of length n
    {
      a = Entropy.random(2, 5);  //Get random number
      simon_q[i] = a;            //Store generated pattern
      if (a == 2)                //Show generated pattern on LEDs
      {
        digitalWrite(2, HIGH);
        delay(q_delay);
        digitalWrite(2, LOW);
        delay(q_delay);
      } else if (a == 3) {
        digitalWrite(3, HIGH);
        delay(q_delay);
        digitalWrite(3, LOW);
        delay(q_delay);
      } else
        digitalWrite(4, HIGH);
      delay(q_delay);
      digitalWrite(4, LOW);
      delay(q_delay);
    }
  }
  while (j < n) {               //Wait for player input
    if (analogRead(A2) > 1000)  //Input for red LED
    {
      simon_a[j] = 2;
      digitalWrite(simon_a[j], HIGH);
      while (analogRead(A2) > 1000) {}  //wait to release button
      delay(ans_delay);
      digitalWrite(simon_a[j], LOW);
      j++;                             //Increment count
    } else if (analogRead(A1) > 1000)  //Input for green LED
    {
      simon_a[j] = 3;
      digitalWrite(simon_a[j], HIGH);
      while (analogRead(A1) > 1000) {}
      delay(ans_delay);
      digitalWrite(simon_a[j], LOW);
      j++;
    } else if (analogRead(A0) > 1000)  //Input for blue LED
    {
      simon_a[j] = 4;
      digitalWrite(simon_a[j], HIGH);
      while (analogRead(A0) > 1000) {}
      delay(ans_delay);
      digitalWrite(simon_a[j], LOW);
      j++;
    }
  }
  for (i = 0; i < n; i++)  //Compare given pattern and player input
  {
    if (simon_q[i] != simon_a[i])  //Incorrect pattern condition
    {
      Serial.println();
      Serial.println("Incorrect, You lose");
      Serial.print("Your score = ");
      Serial.println(score);
      Serial.println();
      for (i = 0; i < n; i++)  //Print given pattern and inputted pattern
      {
        if (simon_q[i] == 2) question = question + "red    ";
        if (simon_q[i] == 3) question = question + "green  ";
        if (simon_q[i] == 4) question = question + "blue   ";

        if (simon_a[i] == 2) your_answer = your_answer + "red    ";
        if (simon_a[i] == 3) your_answer = your_answer + "green  ";
        if (simon_a[i] == 4) your_answer = your_answer + "blue   ";
      }
      Serial.print("Given pattern: ");
      Serial.println(question);
      Serial.print("  Your Answer: ");
      Serial.println(your_answer);
      question = "";
      your_answer = "";
      str = "";
      Serial.println();
      Serial.println("To play again type 'restart'");
      str == "";
      while (str == "")  //wait for "restart" input
      {
        Entropy.random(2, 5);
        str = Serial.readString();
      }
      str.toCharArray(strin, 10);
      if (strcmp(strin, "restart") == 10 || strcmp(strin, "restart") == 0) {
        break;  //exit loop to reset game
      }
    }
  }
  if (strcmp(strin, "restart") == 10 || strcmp(strin, "restart") == 0) {  //Reset game values
    score = 0;
    flag = 1;
    n = 1;
    j = 0;
    str = "start";
    str.toCharArray(strin, 10);
    int simon_q[50] = {}, simon_a[50] = {};
    if (strcmp(apple, "dynamic") == 10 || strcmp(apple, "dynamic") == 0) { q_delay = 500; }
  }
  if (flag == 0) {  //Correct input condition
    Serial.println("Correct");
    score++;
    n++;
    j = 0;
    if (strcmp(apple, "dynamic") == 10 || strcmp(apple, "dynamic") == 0) {  //Dynamic game mode code
      if (score % 2 == 0 && q_delay > 110) {                                //Reduce delay by 50 ms after every 2 correct answers
        q_delay = q_delay - 50;
      }
    }
  }
  flag = 0;
}
