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
	total = int(lines[0].split()[1]) // 1024
	free = int(lines[1].split()[1]) // 1024
	return total, free

while True:
	os.system("clear")
	print("DevNode Status")
	print("-----")
	print("uptime:", get_uptime())
	total, free = get_mem()
	print("RAM:", total-free, "MB used /", total, "MB")
	time.sleep(2)
