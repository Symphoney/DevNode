Start of DevNode AI Companion

This is a project where I work on my linux, hardware, python, c++, and AI

Raspberry Pi based development node for:
- System monitoring
- Hardware feedback UI
- AI Assistant Experimentation
- Embedded Python learning

## Hardware Progress
- Getting comfortable using SSH
- Integrated RGB LED with Rasp Pi GPIO (Raspberry Pi 3 B+)
- Verified red, green, and blue channel control in C++

(This was an exciting step refamiliarizing myself with g++ and understanding the pin board as well as this library)
Just getting comfortable with APIs and using them, while considering multiple ideas for where this project is going.
To note, there is an end goal with this project and it's not just practicing small things.

## RGB LED Progress - System-State Feedback
- LED color reflects system memory usage
- Blue = Low, Green = Medium, Red = High
- Reads memory data from proc/meminfo
- Updates every 2 seconds

(During this process, I also learned of the linux command - mv - to move files from folders)

### Pet State Controller (C++)
- Added basic command-based RGB LED state controller with arguments in main!
- Supports pet-like states like happy, idle, alert, thinking, and error
- Intended for future project feedback layer for incoming project interface

### Behavior Loop (Python + C++)
- Python monitoring loop reads mem usage
- Uses 'MemAvailable' for accurate RAM state calculation
- Tracks prev LED state to avoid unnecessary hardware updates
- Intro to transitional states like 'thinking' before switching into a more active state

Goals after this:
- Refactor code a bit to clean up the parts and polish repo
- Make a manual command interface in Python for reusability and to clean up the hardcoding
- Decide and start using one of the other hardware pieces from the arduino kit
