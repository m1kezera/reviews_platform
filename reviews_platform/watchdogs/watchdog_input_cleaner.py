import os
import json
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# CONFIGURAÇÃO DE PASTAS
RAW_INPUT_FOLDER = "C:/Users/mikam/OneDrive/Desktop/reviews_platform/raw_input"
RAW_ARCHIVE_FOLDER = "C:/Users/mikam/OneDrive/Desktop/reviews_platform/raw_archive"
NEW_DATA_FOLDER = "C:/Users/mikam/OneDrive/Desktop/reviews_platform/new_data"

os.makedirs(RAW_INPUT_FOLDER, exist_ok=True)
os.makedirs(RAW_ARCHIVE_FOLDER, exist_ok=True)
os.makedirs(NEW_DATA_FOLDER, exist_ok=True)

# HEURÍSTICA SIMPLES DE SPAM
def is_spam(comment):
    if not comment:
        return True
    comment = comment.lower()
    return (
        len(comment.strip().split()) < 3 or
        "buy now" in comment or
        "click here" in comment or
        comment.count("!") > 5
    )

# NORMALIZADOR DE CAMPOS
def clean_review(raw):
    return {
        "user_id": f"user_{raw.get('user', raw.get('user_id', 'unknown'))}",
        "product_id": f"prod_{raw.get('product', raw.get('product_id', 'unknown'))}",
        "comment": raw.get("review", raw.get("comment", "")).strip(),
        "rating": int(raw.get("stars", raw.get("rating", 0))),
        "date": raw.get("timestamp", raw.get("date", datetime.now().isoformat())),
        "spam": is_spam(raw.get("review", raw.get("comment", "")))
    }

def process_raw_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        if not isinstance(raw_data, list):
            raw_data = [raw_data]

        cleaned = [clean_review(r) for r in raw_data]

        # Nome do arquivo final organizado
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"batch_cleaned_{timestamp}.json"
        dest_path = os.path.join(NEW_DATA_FOLDER, filename)

        with open(dest_path, "w", encoding="utf-8") as out:
            json.dump(cleaned, out, indent=2)
        print(f"[✓] Cleaned batch saved: {filename}")

        # Mover o original para o arquivo de histórico
        archive_path = os.path.join(RAW_ARCHIVE_FOLDER, os.path.basename(path))
        os.rename(path, archive_path)
        print(f"[→] Raw file archived: {os.path.basename(path)}")

    except Exception as e:
        print(f"[ERROR] Failed to process {path}: {e}")

class RawHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".json"):
            time.sleep(1)
            process_raw_file(event.src_path)

if __name__ == "__main__":
    print(f"👁️ Watching raw input folder: {RAW_INPUT_FOLDER}")
    observer = Observer()
    observer.schedule(RawHandler(), path=RAW_INPUT_FOLDER, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
