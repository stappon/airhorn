#include "application.h"

// disable wifi on boot
SYSTEM_MODE(SEMI_AUTOMATIC);

void setup()
{
	Serial.begin(9600);
}

void loop()
{
	delay(1000);
	Serial.println("DISRUPT");
}