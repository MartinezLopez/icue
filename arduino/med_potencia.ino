#include <SimpleModbusSlave.h>

#define ADDRESS 0x03
#define ID_NUM 0x04

#define PIN 1

enum {
  ID,
  W,
  DBM,
  LAMBDA,
  READ,
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
  double m;
  double n;
  switch(holdingRegs[LAMBDA]) {
    case 1: //820 nm
      m = 0.011353;
      n = 51.484238;
      break;
    case 2: //1300 nm
      m = 0.014147;
      n = 65.986571;
      break;

    case 3: //LD
      m = 0.015471;
      n = 66.701456;
      break;

    default:
      m = 1;
      n = 0;
  }
  
  double volts = meas*5000.0/1024.0; //in mvolts
  double pow_dbm = (m*volts-n);
  double pow_w = dBm_to_nw(pow_dbm);
  
  holdingRegs[DBM] = (pow_dbm) * (-100);
  holdingRegs[W] = pow_w * 100;
  holdingRegs[READ] = volts;
}

double dBm_to_nw(double dBm) {
  double expo = dBm/10.0 + 3;
  double nw = pow(10, expo);
  return nw;
}
