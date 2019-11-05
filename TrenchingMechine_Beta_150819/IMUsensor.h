#include "I2Cdev.h"
#include "MPU6050.h" //uc1508
//c1508 #include "MPU6050_6Axis_MotionApps20.h"

#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif

MPU6050 accelgyro1(0x68);
MPU6050 accelgyro2(0x69);

int16_t ax1, ay1, az1;
int16_t gx1, gy1, gz1;

int16_t ax2, ay2, az2;
int16_t gx2, gy2, gz2;


// ===== Output Data Sensor IMU =====
//#define OUTPUT_BINARY_ACCELGYRO //nilai accelero dan gyro dalam bentuk 16bit binary, mudah untuk diparsing
#define OUTPUT_READABLE_ACCELGYRO //nilai accelero dan gyro bisa dibaca oleh manusia
// ==================================

void IMU_setup(){
  #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
      Wire.begin();
  #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
      Fastwire::setup(400, true);
  #endif

//  Serial.begin(38400);

//  Serial.println("Initializing I2C devices...");
  accelgyro1.initialize();
  accelgyro2.initialize();
  Serial.println(accelgyro1.testConnection() ? "MPU6050 1 connection successful" : "MPU6050 1 connection failed");
  Serial.println(accelgyro2.testConnection() ? "MPU6050 2 connection successful" : "MPU6050 2 connection failed");
}

void IMU_read(){
  accelgyro1.getMotion6(&ax1, &ay1, &az1, &gx1, &gy1, &gz1);
  accelgyro2.getMotion6(&ax2, &ay2, &az2, &gx2, &gy2, &gz2);
}

void IMU_display(){
  
    #ifdef OUTPUT_READABLE_ACCELGYRO
        // display tab-separated accel/gyro x/y/z values
        Serial.print("MPU1:\t");
        Serial.print(ax1); Serial.print("\t");
        Serial.print(ay1); Serial.print("\t");
        Serial.print(az1); Serial.print("\t");
        Serial.print(gx1); Serial.print("\t");
        Serial.print(gy1); Serial.print("\t");
        Serial.println(gz1);

        Serial.print("MPU2:\t");
        Serial.print(ax2); Serial.print("\t");
        Serial.print(ay2); Serial.print("\t");
        Serial.print(az2); Serial.print("\t");
        Serial.print(gx2); Serial.print("\t");
        Serial.print(gy2); Serial.print("\t");
        Serial.println(gz2);
    #endif

    #ifdef OUTPUT_BINARY_ACCELGYRO
        Serial.write((uint8_t)(ax >> 8)); Serial.write((uint8_t)(ax & 0xFF));
        Serial.write((uint8_t)(ay >> 8)); Serial.write((uint8_t)(ay & 0xFF));
        Serial.write((uint8_t)(az >> 8)); Serial.write((uint8_t)(az & 0xFF));
        Serial.write((uint8_t)(gx >> 8)); Serial.write((uint8_t)(gx & 0xFF));
        Serial.write((uint8_t)(gy >> 8)); Serial.write((uint8_t)(gy & 0xFF));
        Serial.write((uint8_t)(gz >> 8)); Serial.write((uint8_t)(gz & 0xFF));
    #endif
}
