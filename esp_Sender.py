#include <ESP8266WiFi.h>
#include <espnow.h>

#define buttonPin 4 //button

# REPLACE WITH RECEIVER MAC Address
uint8_t broadcastAddress[] = {0x24, 0xA1, 0x60, 0x23, 0x53, 0xC8};

# Structure to send data
typedef struct struct_message {
  int b;
} struct_message;
struct_message OnOrOff;

int buttonState = LOW;
unsigned long lastTime = 0;  
unsigned long timerDelay = 2000;  // send readings timer

# Callback when data is sent
void OnDataSent(uint8_t *mac_addr, uint8_t sendStatus) {
  Serial.print("Last Send Status: ");
  if (sendStatus == 0){
    Serial.println("Delivered");
  }
  else{
    Serial.println("fail");
  }
}
 
void setup() {
  pinMode(buttonPin,INPUT);
  Serial.begin(115200);
 
  # Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  # Init ESP-NOW
  if (esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  # Once ESPNow is successfully Init, we will register for Send CB to
  # get the status of Trasnmitted packet
  esp_now_set_self_role(ESP_NOW_ROLE_CONTROLLER);
  esp_now_register_send_cb(OnDataSent);
  
  # Register peer
  esp_now_add_peer(broadcastAddress, ESP_NOW_ROLE_SLAVE, 1, NULL, 0);
}

void loop() {
  buttonState = digitalRead(buttonPin);
   if (buttonState == 1)
   {
      buttonState = 1;
   }
   else  if (buttonState == 0)
   {
      buttonState = 0;
   }
   OnOrOff.b = buttonState;

    // Send message via ESP-NOW
    esp_now_send(broadcastAddress, (uint8_t *) &OnOrOff, sizeof(OnOrOff));

    lastTime = millis();
  }