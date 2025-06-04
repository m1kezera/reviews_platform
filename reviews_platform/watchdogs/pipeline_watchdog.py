import os
import sys
import time
import json
from pymongo import MongoClient
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Adiciona o caminho absoluto para a pasta behavior_AI
sys.path.append("C:/Users/mikam/OneDrive/Desktop/reviews_platform/behavior_AI")
from profile_generator import analyze_batch_and_generate_profiles

# Configurações
WATCH_FOLDER = "C:/Users/mikam/OneDrive/Desktop/reviews_platform/new_data"
PROCESSED_FOLDER = "C:/Users/mikam/OneDrive/Desktop/reviews_platform/processed"
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "reviews_platform"

# Conexão com MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def process_batch(filepath):
    print(f"[✓] Processing batch file: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        reviews_batch = json.load(f)

    # Enviar batch para IA local processar e salvar no banco
    analyze_batch_and_generate_profiles(reviews_batch, db)

    # Mover arquivo para pasta processed
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)
    dest = os.path.join(PROCESSED_FOLDER, os.path.basename(filepath))
    os.rename(filepath, dest)
    print(f"[→] Batch file moved to: {dest}")

class BatchHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith(".json"):
            return
        time.sleep(1)
        process_batch(event.src_path)

if __name__ == "__main__":
    os.makedirs(WATCH_FOLDER, exist_ok=True)
    observer = Observer()
    observer.schedule(BatchHandler(), path=WATCH_FOLDER, recursive=False)
    observer.start()
    print(f"👁️ Watching folder: {WATCH_FOLDER}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
