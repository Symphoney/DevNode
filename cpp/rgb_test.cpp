#include <wiringPi.h>
#include <iostream>

// Project uses 1k ohm resistors so i expect the light to be dim
// I'm also using the RGB light, common cathode
// gpio version - 2.50

int main()
{
	wiringPiSetupGpio(); // initialize - uses raw broadcom gpio pin numbers

	const int RED = 13; // GPIO13
	const int GREEN = 12; // GPIO12
	const int BLUE = 18; // GPIO18

	// hello from powershell

	pinMode(RED, OUTPUT);
	pinMode(GREEN, OUTPUT);
	pinMode(BLUE, OUTPUT);

	auto allOff = [&]()
	{
		digitalWrite(RED, LOW);
		digitalWrite(GREEN, LOW);
		digitalWrite(BLUE, LOW);
	};

	while (true) 
	{
		allOff();
		digitalWrite(RED, HIGH);
		delay(1000);

		allOff();
		digitalWrite(GREEN, HIGH);
		delay(1000);

		allOff();
		digitalWrite(BLUE, HIGH);
		delay(1000);
	}

	return 0;
}
