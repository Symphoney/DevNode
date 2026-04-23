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
- Intro to transitional states like 'thinking' before switching into an active state

### LCD1602 Display Integration (C++)
- Integrated LCD1602 display with Raspberry Pi using 4-bit mode
- Debugged issues relating to 4-bit data pin mapping
- Configured contrast with 10k potentiometer
- Successfully displayed static text
- Comments go into wiring overview

## System Arch
Python (logic / monitor) -> C++ (hardware control layer) -> GPIO (physical) -> LED (state) + LCD (text)

### Terminal Dashboard UI
- Created basic terminal dashboard
- Updated it to a curses-based fullscreen terminal dashboard
- Displays RAM usage, uptime, state, and basic face output
- Uses stable terminal rendering over print redraws
- Designed as foundation for boot-to-dashboard ui
- Added bordered layout to dashboard
- Introduced face section for state visualization and made it animated

