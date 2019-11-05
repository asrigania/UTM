/* 
UNDERWATER TRENCHING MECHINE PROJECT
Date: 17 July 2019
Modified: 18 July 2019
          - data axes
          - pubsub
          15 08 19
*/

#include "globalvariable.h"
#include "Sensors.h"
//#include "IMUsensor.h"
//--------------------------------
#include "bladepositions.h"
#include "camerastreaming.h"
#include "dataflow.h"
#include "displayUTM.h"

// Voltage Sensor

// IMU Sensor

// Depth Sensor

// Blade Positon Sensor



// Display

void setup(){
  // Serial
  Serial.begin(38400);
  
  // voltage sensor:
  
  // IMU sensor:
//  IMU_setup();
  axes_setup();
  
  // depth sensor:
  
  // blade positions sensor:

  // Data Flow
  // 1. Ethernet
  eth_setup();

  // MECHINE:
 
  pinMode(blade, OUTPUT);
  pinMode(captor, OUTPUT);
  pinMode(pump, OUTPUT);
  pinMode(led_mechine, OUTPUT);

  // 

  // Display:
  
}

void loop(){
  // cek2:
  cek2();
  
}

void cek2(){
//  Serial.println("cek");
//  IMU_read();
//  Serial.println("readMPU_ok");
//  IMU_display();
    read_axes(); //ypr
///    display_axes();

  
//  eth_UTM();
//  data_pub();
  
//    disp_s();
//  174.045=float adc_v*5/1023;
//  float adc_v=(1023*174.045)/5;
//  Serial.println(adc_v);
}
