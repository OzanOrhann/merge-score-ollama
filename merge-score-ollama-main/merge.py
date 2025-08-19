import json
import time
import requests

# Dosyayı oku
with open("merged_comparison.json", "r") as f:
    data = json.load(f)

fused_data = []

for i, item in enumerate(data): 
    prompt = f"""You are a medical radiology assistant.

Here are two automatically generated chest X-ray reports for the same image:

Report 1: {item['r2gen_caption']}
Report 2: {item['biomedgpt_caption']}

Please merge these into a single, fluent, and medically accurate report. Avoid repetition and contradictions.
Output:"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()["response"].strip()
        item["fused_caption"] = result
        fused_data.append(item)

        print(f"[{i+1}/100] Fused: {item['image_id']}")
        time.sleep(0.8)

    except Exception as e:
        print(f"[{i+1}] Error: {e}")
        continue

with open("fused_reports.json", "w") as f:
    json.dump(fused_data, f, indent=2)
