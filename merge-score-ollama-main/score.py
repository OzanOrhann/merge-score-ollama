import json
import time
import re
import requests

# Dosyaları yükle
with open("fused_reports.json", "r") as f:
    generated_data = json.load(f)

with open("annotation.json", "r") as f:
    annotations = json.load(f)

# annotation.json içindeki TÜM verileri al (train, test, val fark etmeksizin)
all_splits = []
for key in annotations:
    all_splits.extend(annotations[key])

# id → ground-truth rapor eşlemesi
id_to_gt = {item["id"]: item["report"] for item in all_splits}

scored_data = []

for i, item in enumerate(generated_data):
    image_id = item["image_id"]
    gt_report = id_to_gt.get(image_id)

    if not gt_report:
        print(f"[{i+1}] Warning: Ground-truth not found for image_id {image_id}")
        continue

    prompt = f"""You are a medical radiology expert.

Here is the ground truth radiology report:
"{gt_report}"

Please rate each of the following generated reports on a scale from 0 to 10 based on how medically accurate and complete they are compared to the ground truth. Only return three numbers separated by spaces. No explanation.

Report 1 (R2Gen): "{item['r2gen_caption']}"
Report 2 (BiomedGPT): "{item['biomedgpt_caption']}"
Report 3 (Fused): "{item['fused_caption']}"

Scores (in order):"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )

        scores_raw = response.json()["response"].strip()
        print(f"[{i+1}] Raw Mistral response for {image_id}:\n{scores_raw}\n")

        # Ondalıklı sayıları yakala (örnek: 9.5, 8, 10)
        scores = re.findall(r'\d+(?:\.\d+)?', scores_raw)
        scores = [round(float(s)) for s in scores[:3]]  # ilk 3 skoru al, int'e yuvarla

        if len(scores) != 3:
            print(f"[{i+1}] Warning: Invalid score format for image_id {image_id}")
            continue

        item["r2gen_score"] = scores[0]
        item["biomedgpt_score"] = scores[1]
        item["fused_score"] = scores[2]
        scored_data.append(item)

        print(f"[{i+1}/{len(generated_data)}] Scored: {image_id} => {scores}")
        time.sleep(0.8)

    except Exception as e:
        print(f"[{i+1}] Error: {e}")
        continue

# Skorlanan veriyi kaydet
with open("scored_reports.json", "w") as f:
    json.dump(scored_data, f, indent=2)
