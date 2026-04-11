from pet_control import set_state
import os
import time

def get_uptime():
	with open('/proc/uptime', 'r') as f:
		uptime_seconds = float(f.readline().split()[0])
	minutes = int(uptime_seconds/60)
	return str(minutes) + " minutes"

def get_mem():
	with open('/proc/meminfo', 'r') as f:
		lines = f.readlines()

	meminfo = {}
	for line in lines:
		parts = line.split()
		meminfo[parts[0].rstrip(':')] = int(parts[1]) // 1024

	total = meminfo["MemTotal"]
	available = meminfo["MemAvailable"]
	used = total - available

	return used, total

last_state = None

while True:
	os.system("clear")

	used, total = get_mem()

	print("DevNode Status")
	print("--------------")
	print("Uptime:", get_uptime())
	print("RAM Used:", used, "MB /", total, "MB")

	if used < 150:
		set_state("idle")
		state = "idle"
		print("State: IDLE")
	elif used < 300:
		set_state("happy")
		state = "happy"
		print("State: HAPPY")
	else:
		set_state("alert")
		state = "alert"
		print("State: ALERT")

	if state != last_state:
		set_state("thinking")
		time.sleep(1)
		set_state(state)
		last_state = state

	time.sleep(3)
