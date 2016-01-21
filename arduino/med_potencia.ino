#include <SimpleModbusSlave.h>

#define ADDRESS 0x03
#define ID_NUM 0x04

#define PIN 1

enum {
  ID,
  W,
  DBM,
  LAMBDA,
  HOLDING_REGS_SIZE
};

unsigned int holdingRegs[HOLDING_REGS_SIZE];

void setup() {
  modbus_configure(&Serial, 9600, SERIAL_8N2, ADDRESS, 2, HOLDING_REGS_SIZE, holdingRegs); //TX enable pin 2 (por eso hay un 2 ahi)
  holdingRegs[ID] = ID_NUM;
}

void loop() {
  modbus_update();
  
  power_update();
  
}

void power_update() {
  int meas = analogRead(PIN);
  float m;
  float n;
  switch(holdingRegs[LAMBDA]-256) {
    case 1: //820 nm
      m = 7.53/103;
      n = 60.8;
      break;
    case 2: //1300 nm
      m = 17.0/213.0;
      n = 70.81;
      break;

    case 3:
      m = 127.0/1605.0;
      n = 84.54;
      break;

    default:
      m = 1;
      n = 0;
  }
  
  int pow_dbm = (m*meas-n) * (-100);
  int pow_w = dBm_to_nw(float(pow_dbm)/(-100.0));
  
  holdingRegs[DBM] = pow_dbm;
  holdingRegs[W] = pow_w;
}

int dBm_to_nw(float dBm) {
  float expo = dBm/10.0 + 3;
  double nw = pow(10, expo);
  int nw_100 = nw*100.0;
  return nw_100;
}

  
