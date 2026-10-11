from datetime import datetime
from pathlib import Path
import json
import re
import time

import requests


project_root = Path(__file__).resolve().parent.parent

prompt_path = project_root / "prompts" / "zero_shot_01.txt"
response_path = project_root / "runs" / "zero_shot_01_response.txt"
code_path = project_root / "generated_code" / "zero_shot_01.py"
trace_path = project_root / "runs" / "trace.jsonl"

model = "qwen3:4b"
prompt = prompt_path.read_text(encoding="utf-8")

start = time.time()

response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "stream": False,
        "think": False,
    },
    timeout=600,
)

response.raise_for_status()

answer = response.json()["message"]["content"]
duration = time.time() - start

response_path.write_text(answer, encoding="utf-8")

code_block = re.search(
    r"```(?:python)?\s*(.*?)```",
    answer,
    flags=re.DOTALL,
)

if code_block:
    generated_code = code_block.group(1).strip()
else:
    generated_code = answer.strip()

code_path.write_text(generated_code, encoding="utf-8")

trace = {
    "timestamp": datetime.now().isoformat(),
    "model": model,
    "prompt": prompt,
    "response": answer,
    "duration_seconds": round(duration, 2),
    "code_file": "generated_code/zero_shot_01.py",
}

with trace_path.open("a", encoding="utf-8") as file:
    file.write(json.dumps(trace, ensure_ascii=False) + "\n")

print(f"Dauer: {duration:.2f} Sekunden")
print(f"Antwort gespeichert: {response_path}")
print(f"Code gespeichert: {code_path}")
print(f"Trace gespeichert: {trace_path}")