import subprocess

def set_state(state):
	try:
		subprocess.run(["sudo", "./cpp/pet_state", state], check=True)
	except subprocess.CalledProcessError:
		print("Failed to set state:", state)

if __name__ == "__main__":
	set_state("thinking") # Example
