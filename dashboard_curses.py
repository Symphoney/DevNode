from ai_client import ask_ai
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
		return "IDLE", ["-.-", "o.o"]
	elif used < 300:
		return "THINKING", [".-.", "._."]
	else:
		return "ALERT", ["x.x", "!!"]

def safe_addstr(win, y, x, text, attr=0):
	height, width = win.getmaxyx()
	if 0 <= y < height and 0 <= x < width:
		try:
			win.addstr(y, x, text[:max(0, width - x - 1)], attr)
		except curses.error:
			pass

def draw_box(win, y, x, h, w, title=None):
	height, width = win.getmaxyx()

	if y < 0 or x < 0 or y + h > height or x + w > width:
		return

	# corners
	safe_addstr(win, y, x, "+")
	safe_addstr(win, y, x + w - 1, "+")
	safe_addstr(win, y + h - 1, x, "+")
	safe_addstr(win, y + h - 1, x + w - 1, "+")

	# horizontal
	for i in range(x + 1, x + w - 1):
		safe_addstr(win, y, i, "-")
		safe_addstr(win, y + h - 1, i, "-")

	# vertical
	for i in range(y + 1, y + h - 1):
		safe_addstr(win, i, x, "|")
		safe_addstr(win, i, x + w - 1, "|")

	if title:
		title_text = " " + title + " "
		safe_addstr(win, y, x + 2, title_text)

def chat_mode(stdscr):
	curses.curs_set(1)
	stdscr.nodelay(False)
	stdscr.timeout(-1)

	prompt = ""
	response = "I am your oracle, ask me something. Press q on an empty prompt to return."

	while True:
		stdscr.erase()
		height, width = stdscr.getmaxyx()

		draw_box(stdscr, 1, 2, height - 2, width - 4, " Chat Mode ")

		safe_addstr(stdscr, 3, 4, "DevNode AI")
		safe_addstr(stdscr, 5, 4, "Response:")
		safe_addstr(stdscr, 6, 4, response[:width - 8])

		safe_addstr(stdscr, height - 5, 4, "Type message. Enter to send.")
		safe_addstr(stdscr, height - 4, 4, "Empty q -> returns to dashboard.")
		safe_addstr(stdscr, height - 2, 4, "> " + prompt)

		stdscr.refresh()

		key = stdscr.getch()

		if key == 10 or key == 13:
			if prompt.strip() != "":
				response = ask_ai(prompt)
				prompt = ""
			continue

		if key == 127 or key == curses.KEY_BACKSPACE:
			prompt = prompt[:-1]
			continue

		if prompt == "" and key == ord('q'):
			break

		if 32 <= key <= 126:
			if len(prompt) < width - 10:
				prompt += chr(key)

	curses.curs_set(0)
	stdscr.nodelay(True)
	stdscr.timeout(200)

def main(stdscr):
	curses.curs_set(0)
	stdscr.nodelay(True)
	stdscr.timeout(200)

	while True:
		stdscr.erase()
		height, width = stdscr.getmaxyx()

		used, total = get_mem()
		uptime = get_uptime()
		state, face_frames = get_state(used)

		frame_index = int(time.time() * 3) % len(face_frames)
		face = face_frames[frame_index]

		# min size
		if height < 20 or width < 50:
			safe_addstr(stdscr, 0, 0, "Window too small. Resize terminal.")
			stdscr.refresh()
			key = stdscr.getch()
			if key == ord('q'):
				break
			time.sleep(1)
			continue

		panel_w = 50
		panel_h = 18
		panel_x = (width - panel_w) // 2
		panel_y = (height - panel_h) // 2


		draw_box(stdscr, panel_y, panel_x, panel_h, panel_w, " DevNode ")

		# title
		safe_addstr(stdscr, panel_y + 2, panel_x + 3, "System Status")

		# info section
		safe_addstr(stdscr, panel_y + 4, panel_x + 3, "RAM:    {} MB / {} MB".format(used, total))
		safe_addstr(stdscr, panel_y + 5, panel_x + 3, "Uptime: {}".format(uptime))
		safe_addstr(stdscr, panel_y + 6, panel_x + 3, "State:  {}".format(state))

		# face box
		face_box_y = panel_y + 8
		face_box_x = panel_x + 3
		face_box_w = panel_w - 6
		face_box_h = 5


		draw_box(stdscr, face_box_y, face_box_x, face_box_h, face_box_w, " Face ")

		face_x = face_box_x + (face_box_w - len(face)) // 2
		face_y = face_box_y + face_box_h // 2
		safe_addstr(stdscr, face_y, face_x, face)

		# footer
		safe_addstr(stdscr, panel_y + panel_h - 2, panel_x + 3, "Press c to chat | q to quit")

		stdscr.refresh()

		key = stdscr.getch()
		if key == ord('q'):
			break
		elif key == ord('c'):
			chat_mode(stdscr)

		time.sleep(1)

if __name__ == "__main__":
	curses.wrapper(main)
