import os
import json
import requests

API_KEY = os.environ.get("OPENROUTER_API_KEY")
MODEL = os.environ.get("OPENROUTER_MODEL", "google/gemma-3-12b-it:free")

MODELS = [
		"google/gemma-3-12b-it:free",
		"qwen/qwen3-coder:free",
		"nvidia/nemotron-3-super-120b-a12b:free"
	]

def ask_ai(prompt):
	if not API_KEY:
		return "[No API key identified] " + prompt


	url = "https://openrouter.ai/api/v1/chat/completions"

	headers = {
		"Authorization": "Bearer " + API_KEY,
		"Content-Type": "application/json"
	}

	for model in MODELS:
		data = {
			"model": model,
			"messages": [{"role": "user", "content": "Respond briefly in a calm, stealthy, slightly cryptic tone. " + prompt}]
		}

		try:
			response = requests.post(url, headers=headers, data=json.dumps(data))
			result = response.json()

			if "choices" in result:
				text = result["choices"][0]["message"]["content"]
				return text[:800]


			if "error" in result:
				err = result["error"]

				if err.get("code") == 429:
					continue # moving on to next model

				return "Kor intercepted interference: " + err.get("message", str(err))

			return "Unexpected resp: " + str(result)
		except Exception:
			continue # try next model

	return "Kor don't kor no more"

