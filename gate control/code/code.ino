//Libraries
#include <SPI.h>//https://www.arduino.cc/en/reference/SPI
#include <MFRC522.h>//https://github.com/miguelbalboa/rfid
#include <HTTPClient.h> 
#include <WiFi.h>
#include <Servo_ESP32.h>
#include <LiquidCrystal_I2C.h>

// Create the lcd object address 0x3F and 16 columns x 2 rows 
LiquidCrystal_I2C lcd (0x27, 16,2);  //

//Constants
#define SS_PIN 5
#define RST_PIN 2


//Parameters
const int ipaddress[4] = {103, 97, 67, 25};

//Variables
byte nuidPICC[4] = {0, 0, 0, 0};
MFRC522::MIFARE_Key key;
MFRC522 rfid = MFRC522(SS_PIN, RST_PIN);

String uidString;
bool tagFound;

//Servo motor
static const int servoPin = 14; //printed G14 on the board
String gateState = "closed";

Servo_ESP32 servo1;
int angle = 0;
int angleStep = 10;
int angleMin = 90;
int angleMax = 180;

int greenLED = 4;
int redLED = 27;

//Ultrasonic sensor pins
int trigPin = 13;
int echoPin = 12;
int duration;
int distance;

unsigned long elapsedTime;
const unsigned long period = 1000;
unsigned long startMillis;

//Add WIFI data
const char* ssid = "Msimisi";              //Add your WIFI network name 
const char* password =  "abcdefgh";           //Add WIFI password

//Variables used in the code
//String LED_id = "1";                  //Just in case you control more than 1 LED
//bool toggle_pressed = false;          //Each time we press the push button    
String data_to_send = "";             //Text data to send to the server
unsigned int Actual_Millis, Previous_Millis;
int refresh_time = 200;               //Refresh rate of connection to website (recommended more than 1s)


void setup()
{
   Serial.begin(115200);
    delay(10);

    // We start by connecting to a WiFi network

    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
    
  Actual_Millis = millis();               //Save time for refresh loop
  Previous_Millis = Actual_Millis; 

  
   
  //Init Serial USB
  //Serial.begin(115200);
  Serial.println(F("Initialize System"));
  //init rfid D8,D5,D6,D7
  SPI.begin();
  rfid.PCD_Init();

  Serial.print(F("Reader :"));
  rfid.PCD_DumpVersionToSerial();

  
  startMillis = millis();
  
  pinMode(redLED, OUTPUT);
  pinMode(greenLED, OUTPUT);

  pinMode(trigPin, OUTPUT); 
  pinMode(echoPin, INPUT);

  servo1.attach(servoPin);

   // Initialize the LCD connected 
  lcd.begin ();
  
  // Turn on the backlight on LCD. 
  lcd.backlight ();
}


void loop()
{
    readRFID();
  
    //We make the refresh loop using millis() so we don't have to sue delay();
    Actual_Millis = millis();
    elapsedTime = millis();

    if(uidString != NULL)
    {
      digitalWrite(redLED, LOW);
      if(Actual_Millis - Previous_Millis > refresh_time)
      {
        //Previous_Millis = Actual_Millis;  
        if(WiFi.status()== WL_CONNECTED)                   //Check WiFi connection status 
        { 
          HTTPClient http;                                  //Create new client
          
          data_to_send = "selectVehicle=" + uidString;
          
          //Begin new connection to website       
          http.begin("https://tollcollectionproject.000webhostapp.com/select.php");   //Indicate the destination webpage 
          http.addHeader("Content-Type", "application/x-www-form-urlencoded");         //Prepare the header
          
          int response_code = http.POST(data_to_send);                                //Send the POST. This will give us a response code
    
          Serial.println(data_to_send);
          
          //If the code is higher than 0, it means we received a response
          if(response_code > 0)
          {
            Serial.println("HTTP code " + String(response_code));                     //Print return code
      
            if(response_code == 200)                                                //If code is 200, we received a good response and we can read the echo data
            { 
              String response_body = http.getString();                                //Save the data comming from the website
              Serial.print("Server reply: ");                                         //Print data to the monitor for debug
              Serial.println(response_body); 
              Serial.print("response body = ");
              Serial.println(response_body);
    
              if(response_body.indexOf("Vehicle not registered.") != -1)
              {
                digitalWrite(redLED, HIGH);
                lcd.clear();
                lcd.print("NOT REGISTERED.");
                lcd.setCursor(0, 1);
                lcd.print("<<BRANCH OFF.");
                delay(3000); 
                uidString = "";
              }
    
              if(response_body.indexOf("Insufficient funds.") != -1)
              {
                digitalWrite(redLED, HIGH);
                delay(5000);
                digitalWrite(redLED, LOW);
                lcd.clear();
                lcd.print("LOW FUNDS.");
                lcd.setCursor(0, 1);
                lcd.print("<<BRANCH OFF.");
                delay(3000);
                uidString = "";
              }
              
              else if(response_body.indexOf("Transaction successful.") != -1)
              {
                digitalWrite(greenLED, HIGH);
                int vehiclePosition = detectVehicle();

                lcd.clear();
                lcd.print("WELCOME.");
                lcd.setCursor(0, 1);
                lcd.print("DRIVE SAFE.");
                //delay(3000);
                //uidString = "";

                openGate();
                delay(8000);
                closeGate();

                uidString = "";

                /*
                while(1)
                {
                  if(vehiclePosition < 10)//&& gateState == "closed")
                  {
                    openGate();
                    gateState = "open"; 
                    Serial.println("GATE OPEN");
                    digitalWrite(greenLED, LOW);
                    delay(5000);
                    closeGate();
                    break;
                  }
                }

                */

              /*  else if(vehiclePosition > 10 && gateState == "open")
                  closeGate();
                  gateState = "closed";
                  Serial.println("GATE OPEN");
              }*/
              }
            }//End of response_code = 200
           }//END of response_code > 0
          
          else
          {
           Serial.print("Error sending POST, code: ");
           Serial.println(response_code);
           lcd.clear();
           lcd.print("SYSTEM DOWN.");
           lcd.setCursor(0, 1);
           lcd.print("<<BRANCH OFF.");

           

           delay(3000);
           uidString = "";
          }
           
          http.end();     //End the connection
        }//END of WIFI connected
        else{
          Serial.println("WIFI connection error");
          lcd.clear();
          lcd.print("SYSTEM DOWN.");
          lcd.setCursor(0, 1);
          lcd.print("<<BRANCH OFF.");
        }
      }
    //}

   
}

   if(uidString == NULL)   //if RFID tag is not found
    {
      digitalWrite(redLED, HIGH);
      Serial.println("RFID tag not found.");

      lcd.clear();
      lcd.print("JOIN TOLL GATE.");
    }
}


 /* function readRFID */

 
void readRFID() { 
  ////Read RFID card

  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;
  }
  // Look for new 1 cards
  if ( ! rfid.PICC_IsNewCardPresent())
  {
    //tagFound = false;
    return;
  }
    

  // Verify if the NUID has been readed
  if (  !rfid.PICC_ReadCardSerial())
    return;

  // Store NUID into nuidPICC array
  for (byte i = 0; i < 4; i++) {
    nuidPICC[i] = rfid.uid.uidByte[i];
    Serial.print(nuidPICC[i]);
  }
  Serial.println(" ");
  Serial.print(F("RFID In dec: "));
  printDec(rfid.uid.uidByte, rfid.uid.size);
  Serial.println();


 //rfid.PICC_ReadCardSerial();
  Serial.print("Tag UID: ");
  uidString = String(rfid.uid.uidByte[0]) + String(rfid.uid.uidByte[1]) + String(rfid.uid.uidByte[2]) + String(rfid.uid.uidByte[3]);
    Serial.print("uid string = ");
  Serial.println(uidString);

  // Halt PICC
  rfid.PICC_HaltA();

  // Stop encryption on PCD
  rfid.PCD_StopCrypto1();

}

void printHex(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}



/**
   Helper routine to dump a byte array as dec values to Serial.
*/


void printDec(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    //Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], DEC);
  }
}


int detectVehicle()
{
  digitalWrite(trigPin, LOW); 
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH); 
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance= duration*0.034/2;
  Serial.println(distance);
  delay(100);

  return distance;
}


void closeGate()
{
  for(int angle = 90; angle <= angleMax; angle +=angleStep)
  {
    servo1.write(angle);
    Serial.println(angle);
    delay(20);
  }
}

void openGate()
{
  for(int angle = 180; angle >= angleMin; angle -=angleStep)
  {
    servo1.write(angle);
    Serial.println(angle);
    delay(20);
  }
}



/**
   Helper routine to dump a byte array as hex values to Serial.
*/
