import requests
import time
import json
from pathlib import Path
from datetime import datetime

url = "http://localhost:11434/api/chat"

prompt = "Explain pandas in exactly one short sentence."

data = {
    "model": "qwen3:4b",
    "messages": [
        {"role": "user", "content": prompt}
    ],
    "stream": False,
    "think": False
}

start = time.time()
response = requests.post(url, json=data)
response.raise_for_status()

result = response.json()
duration = time.time() - start

answer = result["message"]["content"]

print(answer)
print(f"Dauer: {duration:.2f} Sekunden")

Path("runs").mkdir(exist_ok=True)

trace = {
    "timestamp": datetime.now().isoformat(),
    "model": "qwen3:4b",
    "prompt": prompt,
    "response": answer,
    "duration_seconds": round(duration, 2)
}

with open("runs/trace.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(trace, ensure_ascii=False) + "\n")