#include "application.h"

#define CLAMP(x, low, high)  (((x) > (high)) ? (high) : (((x) < (low)) ? (low) : (x)))

// servo globals
#define SERVO_PIN D0
#define SERVO_STEP_DELAY_MS 4.5 // milliseconds required to travel 1 degree
#define SERVO_MAX_DEGREES 180
Servo servo;

// horn on/off positions
#define HORN_ENGAGED_POS 120
#define HORN_DISENGAGED_POS 180

// debug LED
#define LED_PIN D1


/* Setup */
void setup()
{
	// hook up debugging machinery
	Serial.begin(9600);
	pinMode(LED_PIN, OUTPUT);

	// initialize servo
	pinMode(SERVO_PIN, OUTPUT);
	servo.attach(SERVO_PIN);
	go_to_position_in_degrees(HORN_DISENGAGED_POS);

	// register the Spark function
	Spark.function("disrupt", disrupt);

	// blink the LED to show that we've begun
	digitalWrite(LED_PIN, HIGH);
	delay(1000);
	digitalWrite(LED_PIN, LOW);
}

/* Loop */
void loop()
{} // no-op - API callback drives the action


/* API callback */
int disrupt(String arg)
{
	// LED on
	digitalWrite(LED_PIN, HIGH);

	// BRAAAAAAAAAAP
	uint16_t pos = arg.toInt();
	blow_that_horn(pos);

	// LED off
	digitalWrite(LED_PIN, LOW);

	// SUCCESS IS THE ONLY OPTION
	return 0; 
}


/* Utility functions */

// disrupt the eardrum industry
void blow_that_horn(uint16_t duration_ms)
{
	go_to_position_in_degrees(HORN_ENGAGED_POS);
	delay(duration_ms);
	go_to_position_in_degrees(HORN_DISENGAGED_POS);
}

void go_to_position_in_degrees(uint8_t target_pos)
{
	// get the current and clamped target positions
	uint8_t pos = servo.read();
	target_pos = CLAMP(target_pos, 0, SERVO_MAX_DEGREES); // assume range is [0:max_degrees]

	// if there's nothing to do, bail
	if (pos == target_pos)
		return;

	// SO EASY!
	servo.write(target_pos);
	delay(abs(target_pos - pos) * SERVO_STEP_DELAY_MS);
}