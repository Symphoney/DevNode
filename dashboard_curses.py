import curses
import time

def get_mem():
	with open('/proc/meminfo', 'r') as f:
		lines = f.readlines()

	meminfo = {}
	for line in lines:
		parts = line.split()
		meminfo[parts[0].rstrip(':')] = int(parts[1])

	total = meminfo["MemTotal"] // 1024
	available = meminfo["MemAvailable"] // 1024
	used = total - available

	return used, total

def get_uptime():
	with open('/proc/uptime', 'r') as f:
		uptime_seconds = float(f.readline().split()[0])
	minutes = int(uptime_seconds / 60)
	return str(minutes) + " min"

def get_state(used):
	if used < 150:
		return "IDLE", "-.-"
	elif used < 300:
		return "THINKING", "o.o"
	else:
		return "ALERT", "x.x"

def draw_centered(stdscr, y, text):
	height, width = stdscr.getmaxyx()
	x = max(0, (width - len(text)) // 2)
	stdscr.addstr(y, x, text)

def main(stdscr):
	curses.curs_set(0)
	stdscr.nodelay(True)
	stdscr.timeout(200)

	while True:
		stdscr.erase()
		used, total = get_mem()
		uptime = get_uptime()
		state, face = get_state(used)

		draw_centered(stdscr, 1, "=== DevNode ===")
		draw_centered(stdscr, 3, "System Status")
		draw_centered(stdscr, 4, "---------------")
		draw_centered(stdscr, 6, "RAM: {} MB / {} MB".format(used, total))
		draw_centered(stdscr, 7, "Uptime: {}".format(uptime))
		draw_centered(stdscr, 8, "State: {}".format(state))
		draw_centered(stdscr, 11, face)

		draw_centered(stdscr, 14, "Press q to quit")

		stdscr.refresh()

		key = stdscr.getch()
		if key == ord('q'):
			break

		time.sleep(1)

if __name__ == "__main__":
	curses.wrapper(main)
