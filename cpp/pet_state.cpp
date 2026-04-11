#include <wiringPi.h>
#include <iostream>
#include <string>

const int RED = 13;
const int GREEN = 12;
const int BLUE = 18;

void allOff()
{
	digitalWrite(RED, LOW);
	digitalWrite(GREEN, LOW);
	digitalWrite(BLUE, LOW);
}

void setColor (bool redOn, bool greenOn, bool blueOn)
{
	digitalWrite(RED, redOn ? HIGH : LOW);
	digitalWrite(GREEN, greenOn ? HIGH : LOW);
	digitalWrite(BLUE, blueOn ? HIGH : LOW);
}

void blinkColor(bool redOn, bool greenOn, bool blueOn, int times, int delayMs)
{
	for (int i = 0; i < times; i++)
	{
		setColor(redOn, greenOn, blueOn);
		delay(delayMs);
		allOff();
		delay(delayMs);
	}
}

int main(int argc, char* argv[])
{
	if (wiringPiSetupGpio() == -1)
	{
		std::cerr << "Failure to initialize GPIO." << '\n'; // doc explained -1 if error, else 0
		return 1;
	}

	pinMode(RED, OUTPUT);
	pinMode(GREEN, OUTPUT);
	pinMode(BLUE, OUTPUT);

	allOff();

	if (argc < 2)
	{
		std::cout << "Usage: sudo ./pet_state <state>" << '\n';
		std::cout << "States: idle, happy, thinking, alert, error, off" << '\n';
		return 1;
	}

	std::string state = argv[1];

	if (state == "idle")
	{
		setColor(false, false, true); // blue
		std::cout << "Pet: IDLE" << '\n';
	}
	else if (state == "happy")
	{
		setColor(false, true, false); // green
		std::cout << "Pet: HAPPY" << '\n';
	}
	else if (state == "alert")
	{
		setColor(true, false, false); // red
		std::cout << "Pet: ALERT" << '\n';
	}
	else if (state == "error")
	{
		blinkColor(true, false, false, 5, 250);
		std::cout << "Pet: ERROR" << '\n';
	}
	else if (state == "thinking")
	{
		blinkColor(true, false, true, 5, 250); // purpleish
		std::cout << "Pet: THINKING" << '\n';
	}
	else if (state == "off")
	{
		allOff();
		std::cout << "Where pet go?" << '\n';
	}
	else
	{
		std::cout << "Unknown state: " << state << '\n';
		std::cout << "States currently usable: happy, idle, thinking, alert, error, off" << '\n';
		allOff();
		return 1;
	}

	return 0;
}
