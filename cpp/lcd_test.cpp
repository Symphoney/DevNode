#include <wiringPi.h>
#include <lcd.h>
#include <iostream>
#include <unistd.h>

int main()
{
	std::cout << "Starting lcd_test" << '\n';


	if (wiringPiSetupGpio() == -1)
	{
		std::cerr << "Failure to initialize GPIO." << '\n';
		return 1;
	}

	std::cout << "GPIO initialized." << '\n';

	// doing 4 bit since that's what's compatible
	int lcdHandle = lcdInit(2, 16, 4, 25, 24, 23, 17, 27, 22, 0, 0, 0, 0);
	/*
		2 = rows
		16 = columns
		4 = 4-bit mode
		25 = GPIO25 [RS]
		24 = GPIO24 [E]
		0, 0, 0, 0 = unused [D0-D3]
		23 = [d4]
		17 = [d5]
		27 = [d6]
		22 = [d7]
	*/

	if (lcdHandle < 0)
	{
		std::cerr << "lcdInit failed." << '\n';
		return 1;
	}

	std::cout << "lcdInit success. Writing text..." << '\n';

	lcdClear(lcdHandle);

	lcdPosition(lcdHandle, 0, 0);
	lcdPuts(lcdHandle, "Greetings");

	lcdPosition(lcdHandle, 0, 1);
	lcdPuts(lcdHandle, "From DevNode");

	std::cout << "Text written. Sleeping soon." << '\n';
	sleep(10);

	return 0;
}
