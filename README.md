# merge-score-ollama

This repository was developed by **Ozan Orhan** and **İrfan Şenel**.  
It contains scripts for **merging radiology reports** and **scoring them** with evaluation metrics.  
The project is a complementary part of our work on biomedical report generation and LLM-based fusion.

## Project Overview
- **merge.py** → Combines report outputs (e.g., from different models).  
- **score.py** → Evaluates reports using metrics such as **BLEU, ROUGE, METEOR, CIDEr**.  
- JSON files (`fused_reports.json`, `scored_reports.json`) contain intermediate and final results.  

## Related Work
This project is related to our fine-tuning and fusion experiments with:  
- [R2Gen](https://github.com/cuhksz-nlp/R2Gen)  
- [BiomedGPT](https://github.com/taokz/BiomedGPT)  

## Notes
- Developed for **academic purposes only**.  
- Dataset preparation and model training are done separately.  
- This repo focuses only on **merging & scoring** the outputs.  
