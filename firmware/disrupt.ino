#include "application.h"

#define CLAMP(x, low, high)  (((x) > (high)) ? (high) : (((x) < (low)) ? (low) : (x)))

// servo globals
#define SERVO_PIN D0
#define SERVO_STEP_DELAY_MS 4.5 // milliseconds required to travel 1 degree
#define SERVO_MAX_DEGREES 180
Servo servo;


/* Setup */
void setup()
{
	Serial.begin(9600);
	pinMode(SERVO_PIN, OUTPUT);
	servo.attach(SERVO_PIN);
	go_to_position_in_degrees(0);

	delay(1000);
}

/* Loop */
void loop()
{
	disrupt(500);
	delay(2000);
}


/* Utility functions */

// disrupt the eardrum industry
void disrupt(uint16_t duration_ms)
{
	go_to_position_in_degrees(180);
	delay(duration_ms);
	go_to_position_in_degrees(0);
}

void go_to_position_in_degrees(int16_t target_pos)
{
	// get the current and clamped target positions
	int16_t pos = servo.read();
	target_pos = CLAMP(target_pos, 0, SERVO_MAX_DEGREES); // assume range is [0:max_degrees]

	// if there's nothing to do, bail
	if (pos == target_pos)
		return;

	// SO EASY!
	servo.write(target_pos);
	delay(abs(target_pos - pos) * SERVO_STEP_DELAY_MS);
}