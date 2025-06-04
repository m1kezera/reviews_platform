import os
import json
from datetime import datetime
from faker import Faker
from pymongo import MongoClient

# Conexão MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["reviews_platform"]

# Pasta de entrada e saída
RAW_INPUT = "C:/Users/mikam/OneDrive/Desktop/reviews_platform/raw_input"
NEW_DATA = "C:/Users/mikam/OneDrive/Desktop/reviews_platform/new_data"
os.makedirs(NEW_DATA, exist_ok=True)

faker = Faker()

def generate_fake_user(user_id):
    return {
        "user_id": user_id,
        "user_name": faker.name(),
        "user_email": faker.email()
    }

def generate_fake_product(product_id):
    return {
        "product_id": product_id,
        "product_name": faker.catch_phrase(),
        "product_category": faker.word(ext_word_list=["electronics", "books", "fashion", "home", "sports"])
    }

def enrich_review(review):
    # Preencher dados do usuário
    user_data = db["users"].find_one({"user_id": review["user_id"]})
    if not user_data:
        user_data = generate_fake_user(review["user_id"])
        db["users"].insert_one(user_data)

    review["user_name"] = user_data.get("user_name", "Unnamed User")
    review["user_email"] = user_data.get("user_email", "unknown@example.com")

    # Preencher dados do produto
    product_data = db["products"].find_one({"product_id": review["product_id"]})
    if not product_data:
        product_data = generate_fake_product(review["product_id"])
        db["products"].insert_one(product_data)

    review["product_name"] = product_data.get("product_name", "Unnamed Product")
    review["product_category"] = product_data.get("product_category", "uncategorized")

    # Garantir campo de data
    if "date" not in review:
        review["date"] = datetime.now().isoformat()

    return review

def process_raw_batches():
    for filename in os.listdir(RAW_INPUT):
        if filename.endswith(".json"):
            filepath = os.path.join(RAW_INPUT, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                raw_reviews = json.load(f)

            enriched = [enrich_review(r) for r in raw_reviews]

            output_path = os.path.join(NEW_DATA, f"cleaned_{filename}")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(enriched, f, indent=2, ensure_ascii=False)

            # Mover original para arquivo
            archive_path = filepath.replace("/raw_input/", "/raw_archive/")
            os.makedirs(os.path.dirname(archive_path), exist_ok=True)
            os.rename(filepath, archive_path)
            print(f"[✓] Processed and enriched: {filename}")

if __name__ == "__main__":
    process_raw_batches()
