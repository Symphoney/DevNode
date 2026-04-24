def ask_ai(prompt):
	prompt = prompt.lower()

	if "status" in prompt:
		return "System running normally."
	elif "hello" in prompt:
		return "Hello. Currently monitoring systems."
	elif "time" in prompt:
		return "Time is an illusion"
	else:
		return "Processing request but can't actually..."
