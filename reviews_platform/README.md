
*NOTE* : Some commentaries on the codes might be in portuguese, just translate it.

# 🧠 Review Behavior Analysis Platform (MongoDB + Local AI)

A realistic simulation of a smart backend platform for analyzing user reviews with local AI, fully offline processing, MongoDB storage, and automated watchdog orchestration. The project was built for real-world applicability — structured, maintainable, and extendable.

GitHub repository (author): https://github.com/m1kezera

---

## ✅ Features

- ⚙️ Fully automated data pipeline with real-time file monitoring
- 💬 Local AI analysis of:
  - Emotions (via transformer model)
  - Sentiment alignment with user rating
  - Spam detection (in both pre-cleaner and IA layer)
  - Topic mapping
- 👤 Generation of user behavioral profiles
  - Persona tags and labels
  - Trust and risk scoring
  - Natural language summary
  - Actionable insights
- 📦 MongoDB integration with:
  - `reviews` collection (all enriched reviews)
  - `user_evaluation` collection (aggregated user profiles)
  - `users` and `products` created and populated automatically
- 📁 Logs saved in `/logs/behavior_analysis/`
- 🧪 Includes batch simulation with 300+ raw reviews
- 🌐 Ready for future API integration or manual usage

---

## 🗂️ Project Structure

```
reviews_platform/
├── .vscode/
│   └── settings.json              # Adds behavior_AI to Python path
│
├── behavior_AI/
│   ├── emotion_detector.py
│   ├── persona_builder.py
│   ├── profile_generator.py
│   ├── risk_analyzer.py
│   ├── sentiment_tuner.py
│   └── topic_mapper.py
│
├── watchdogs/
│   ├── pipeline_watchdog.py       # Processes structured reviews in /new_data/
│   ├── watchdog_input_cleaner.py  # Cleans raw input data in /raw_input/
│   └── start_watchdogs.py         # Launches both watchdogs together
│
├── new_data/                      # Reviews structured and ready for analysis
├── processed/                     # Fully processed reviews (archived)
├── raw_input/                     # Entry point for raw, unstructured data
├── raw_archive/                   # Archive of raw input files for traceability
├── test_batch/                    # Manual testing files and examples
├── logs/
│   └── behavior_analysis/         # Log summaries of each batch run
│
├── README.md                      # Final documentation file 
```

---

## 🚀 How to Use

### 1. Install dependencies

```bash
pip install transformers pymongo watchdog
```

---

### 2. Run the system

```bash
python start_watchdogs.py
```

This will:
- ✅ Run `watchdog_input_cleaner.py` to structure raw inputs
- ✅ Run `pipeline_watchdog.py` to process structured batches

> ⚠️ All collections are created automatically.  
> ⚠️ All `user_id` and `product_id` values are dynamically registered during processing.

---

### 3. Add Your Data

- 📥 Raw review files → `/raw_input/` (e.g. `raw_batch_volume.json`)
- 📥 Ready-to-use JSON → `/new_data/` (already structured)
- The system works **offline** and is prepared for future REST/API endpoints

---

## 🧠 AI Workflow

1. Each review goes through:
   - Spam detection (rule-based)
   - Sentiment analysis aligned with rating
   - Emotion detection using HuggingFace model
   - Topic extraction
   - Trust scoring

2. A user profile is generated with:
   - Emotional average
   - Common topics
   - Risk analysis
   - Persona classification
   - Summary + insights

---

## 🧾 MongoDB Collections

- **`reviews`** → Enriched individual reviews  
- **`user_evaluation`** → Full behavior profile per user  
- **`users`** → All user IDs are registered automatically  
- **`products`** → All product IDs are registered automatically  

---

## 📦 Volume Testing

Drop `raw_batch_volume.json` into `/raw_input/` to see 300+ entries processed, structured, profiled, and saved.

---

## 💡 Future Integration

This system can be extended to:
- Receive reviews from a live API
- Generate user reports in PDF
- Feed analytics dashboards
- Provide per-user segmentation or personalization engines

---

## 🛠️ Tech Stack

- 🐍 Python
- 🧠 HuggingFace Transformers
- 🍃 MongoDB (local)
- 👀 Watchdog (file monitoring)
- 📂 Offline-first pipeline

---

## 🧑 Author

Published and maintained by [m1kezera](https://github.com/m1kezera)

---
