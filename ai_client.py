import os
import json
import requests

API_KEY = os.environ.get("OPENROUTER_API_KEY")
MODEL = os.environ.get("OPENROUTER_MODEL", "google/gemma-3-12b-it:free")

def ask_ai(prompt):
	if not API_KEY:
		return "[No API key identified] " + prompt

	url = "https://openrouter.ai/api/v1/chat/completions"

	headers = {
		"Authorization": "Bearer " + API_KEY,
		"Content-Type": "application/json"
	}

	data = {
		"model": "google/gemma-3-12b-it:free",
		"messages": [{"role": "user", "content": prompt}]
	}

	try:
		response = requests.post(url, headers=headers, data=json.dumps(data))
		result = response.json()

		if "error" in result:
			return "OpenRouter error: " + str(result["error"])

		if "choices" not in result:
			return "Unexpected resp: " + str(result)

		return result["choices"][0]["message"]["content"]

	except Exception as e:
		return "Error: " + str(e)
