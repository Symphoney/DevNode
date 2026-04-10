#include <wiringPi.h>
#include <iostream>
#include <fstream>
#include <string>
#include <unistd.h>

const int RED = 13;
const int GREEN = 12;
const int BLUE = 18;

void allOff()
{
	digitalWrite(RED, LOW);
	digitalWrite(GREEN, LOW);
	digitalWrite(BLUE, LOW);
}

void setColor(bool redOn, bool greenOn, bool blueOn)
{
	digitalWrite(RED, redOn ? HIGH : LOW); // if redOn is true, HIGH. else LOW - ternary operator
	digitalWrite(GREEN, greenOn ? HIGH : LOW);
	digitalWrite(BLUE, blueOn ? HIGH : LOW);
}

bool getMemoryUsageMB(long &usedMB, long &totalMB)
{
	std::ifstream meminfo("/proc/meminfo");
	if (!meminfo.is_open())
	{
		return false;
	}

	std::string key;
	long value;
	std::string unit;

	long memTotalKB = 0;
	long memAvailableKB = 0;

	while (meminfo >> key >> value >> unit)
	{
		if (key == "MemTotal:")
		{
			memTotalKB = value;
		}
		else if (key == "MemAvailable:")
		{
			memAvailableKB = value;
		}

		if (memTotalKB > 0 && memAvailableKB > 0)
		{
			break;
		}
	}

	if (memTotalKB == 0 || memAvailableKB == 0)
	{
		return false;
	}

	totalMB = memTotalKB / 1024;
	usedMB = (memTotalKB - memAvailableKB) / 1024;
	return true;
}

int main()
{
	if (wiringPiSetupGpio() == -1)
	{
		std::cerr << "Failed to init GPIO." << '\n';
		return 1;
	}

	pinMode(RED, OUTPUT);
	pinMode(GREEN, OUTPUT);
	pinMode(BLUE, OUTPUT);

	allOff();

	while (true)
	{
		long usedMB = 0;
		long totalMB = 0;

		if (!getMemoryUsageMB(usedMB, totalMB))
		{
			std::cerr << "Could not read mem info." << '\n';
			setColor(true, false, false); // red shows when error
			sleep(2);
			continue;
		}

		std::cout << "RAM Used: " << usedMB << " MB / " << totalMB << " MB" <<  '\n';

		if (usedMB < 150)
		{
			setColor(false, false, true); // blue = low
		}
		else if (usedMB < 300)
		{
			setColor(false, true, false); // green = medium
			std::cout << "State: MEDIUM usage (green)" << '\n';
		}
		else
		{
			setColor(true, false, false); // red = high
			std::cout << "State: HIGH usage (red)" << '\n';
		}

		std::cout << "-------" << '\n';
	}

	return 0;
}

