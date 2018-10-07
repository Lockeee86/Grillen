//----------------------------------------
// Grillen | ...wenn Männer kochen
// Programm zwei analoge Ikea Fantast
// und digital DHT22 Sensor
// 
//----------------------------------------
#include <math.h>
#include "DHT.h"

#define DHTPIN 10   
#define DHTTYPE DHT11 //DHT wählen 

#define Grill A2
#define Fleisch2 A1
#define Fleisch  A0
#define ABSZERO 273.15
#define MAXANALOGREAD 1023.0

#define DELAY 50 #250 geht gut!

int ledcolor = 0;
int red = 11; //this sets the red led pin
int green = 12; //this sets the green led pin
int blue = 13; //this sets the blue led pin
byte Kivy;

DHT dht(DHTPIN, DHTTYPE);

// ---- Analog NTC IKEA FANTAST ----------
// Voreistellungen/Erläuterung
//
// Ermittlung der Temperatur mittels NTC-Widerstand
// Version der Funktion bei unbekannter Materialkonstante B
// Erklärung der Parameter:
// T0           : Nenntemperatur des NTC-Widerstands in °C
// R0           : Nennwiderstand des NTC-Sensors in Ohm
// T1           : erhöhte Temperatur des NTC-Widerstands in °C
// R1           : Widerstand des NTC-Sensors bei erhöhter Temperatur in Ohm
// Vorwiderstand: Vorwiderstand in Ohm  
// VA_VB        : Spannungsverhältnis "Spannung am NTC zu Betriebsspannung"
// Rückgabewert : Temperatur

float temp_m1[4];
float temperatur1 = 0;

float temp_m2[4];
float temperatur2 = 0;

float temperature_NTC(float T0, float R0, float T1, float R1, float RV, float VA_VB)
{
 T0+=ABSZERO;  // umwandeln Celsius in absolute Temperatur
 T1+=ABSZERO;  // umwandeln Celsius in absolute Temperatur
 float B= (T0 * T1)/ (T1-T0) * log(R0/R1); // Materialkonstante B
 float RN=RV*VA_VB / (1-VA_VB); // aktueller Widerstand des NTC
 return T0 * B / (B + T0 * log(RN / R0))-ABSZERO;
}

void setup()
{
 Serial.begin(115200);
 //delay(1000);
 //Serial.println("0 ,0 ,0 ,0 ");
 dht.begin();
 pinMode(red, OUTPUT);
 pinMode(green, OUTPUT);
 pinMode(blue, OUTPUT);
 digitalWrite(green, LOW);
 digitalWrite(red, LOW);
 digitalWrite(blue, LOW);
 delay(2000);
}

void loop()
{
 // IKEA Fantast
// float T0=27;    // Nenntemperatur des NTC-Widerstands in °C
// float R0=214000; // Nennwiderstand des NTC-Sensors in Ohm
// float T1=100;   // erhöhte Temperatur des NTC-Widerstands in °C
// float R1=13000;  // Widerstand des NTC-Sensors bei erhöhter Temperatur in Ohm
 
 // Steffen Weber 
 float T0=24;    // Nenntemperatur des NTC-Widerstands in °C
 float R0=240000; // Nennwiderstand des NTC-Sensors in Ohm
 float T1=100;   // erhöhte Temperatur des NTC-Widerstands in °C
 float R1=13100;  // Widerstand des NTC-Sensors bei erhöhter Temperatur in Ohm

// IKEA Fantast 2.
 float T0_temp_fleisch=27;    // Nenntemperatur des NTC-Widerstands in °C
 float R0_temp_fleisch=214000; // Nennwiderstand des NTC-Sensors in Ohm
 float T1_temp_fleisch=100;   // erhöhte Temperatur des NTC-Widerstands in °C
 float R1_temp_fleisch=13000;  // Widerstand des NTC-Sensors bei erhöhter Temperatur in Ohm

 // IKEA Fantast 3.
 float T0_temp_fleisch2=27;    // Nenntemperatur des NTC-Widerstands in °C
 float R0_temp_fleisch2=214000; // Nennwiderstand des NTC-Sensors in Ohm
 float T1_temp_fleisch2=100;   // erhöhte Temperatur des NTC-Widerstands in °C
 float R1_temp_fleisch2=13000;  // Widerstand des NTC-Sensors bei erhöhter Temperatur in Ohm
 
 float Vorwiderstand=10000; // Vorwiderstand in Ohm  
 float temp_grill;
 float temp_fleisch; 
 float temp_fleisch2;   
 int aValue0=analogRead(Grill);
 int aValue1=analogRead(Fleisch);
 int aValue2=analogRead(Fleisch2);
 
// Berechnen bei unbekannter Materialkonstante für Grill
 temp_grill=temperature_NTC(T0, R0, T1, R1, Vorwiderstand, aValue0/MAXANALOGREAD);  
// Berechnen bei unbekannter Materialkonstante für Fleisch
 temp_fleisch=temperature_NTC(T0_temp_fleisch, R0_temp_fleisch, T1_temp_fleisch, R1_temp_fleisch, Vorwiderstand, aValue1/MAXANALOGREAD);
// Berechnen bei unbekannter Materialkonstante für Fleisch 2
 temp_fleisch2=temperature_NTC(T0_temp_fleisch2, R0_temp_fleisch2, T1_temp_fleisch2, R1_temp_fleisch2, Vorwiderstand, aValue2/MAXANALOGREAD);
if (temp_grill <= 0){
  temp_grill = 0;
}
if (temp_fleisch <= 0){
  temp_fleisch = 0;
}
if (temp_fleisch2 <= 0){
  temp_fleisch2 = 0;
}
 // --------- LED An/Aus -------------------------
   while(Serial.available())
  {
    delay(3);   //wait three milliseconds
    if(Serial.available() > 0)  //if there is Serial to read
    {
    /* read the most recent byte */
      Kivy = Serial.read();
      if (Kivy == 49) {
        if (temp_grill< 90) {
          digitalWrite(green, LOW);
          digitalWrite(red, LOW);
          digitalWrite(blue, HIGH);
        }
        if (temp_grill> 90) {
          digitalWrite(green, HIGH);
          digitalWrite(red, LOW);
          digitalWrite(blue, HIGH);
        }   
        if (temp_grill> 100) {
          digitalWrite(green, HIGH);
          digitalWrite(red, LOW);
          digitalWrite(blue, LOW);
        }
        if (temp_grill> 115) {
          digitalWrite(green, LOW);
          digitalWrite(red, HIGH);
          digitalWrite(blue, HIGH);
        }   
        if (temp_grill> 130) {
          digitalWrite(green, LOW);
          digitalWrite(red, HIGH);
          digitalWrite(blue, LOW);
        }   
      }
      else if (Kivy == 48) {
      digitalWrite(green, LOW);
      digitalWrite(red, LOW);
      digitalWrite(blue, LOW);
    }
  }
}
delay(10); // delay for 1/10 of a second

// ---------------- Digital Temp ---------------------------------------------
  float h = dht.readHumidity();
  float t = dht.readTemperature();

// send Data to serial port
  Serial.print((int)roundf(temp_grill));
//  Serial.print("0");
  Serial.print(", ");
  Serial.print((int)roundf(temp_fleisch));
  Serial.print(", ");
  Serial.print((int)roundf(temp_fleisch2));
  Serial.print(", ");
  Serial.print((int)roundf(t));
  Serial.print(", ");
  Serial.println((int)roundf(h)); 


  delay(DELAY);
 }

