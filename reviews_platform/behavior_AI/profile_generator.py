from emotion_detector import detect_emotions
from sentiment_tuner import check_alignment
from topic_mapper import map_topics
from risk_analyzer import analyze_risk
from persona_builder import build_persona
from datetime import datetime
import os

def detect_spam(comment):
    if not comment:
        return True
    comment = comment.lower()
    return (
        len(comment.split()) < 3 or
        "buy now" in comment or
        "click here" in comment or
        comment.count("!") > 5
    )

def generate_profile(user_id, reviews):
    if not reviews:
        return {
            "user_id": user_id,
            "error": "No reviews found"
        }

    texts = [r["comment"] for r in reviews if "comment" in r]
    ratings = [r.get("rating", 0) for r in reviews]
    sentiments = [r.get("sentiment", "neutral") for r in reviews]
    spam_count = sum(1 for r in reviews if r.get("spam") == True)

    emotion_avg = detect_emotions(texts)

    trust_scores = []
    for r in reviews:
        result = check_alignment(r["comment"], r.get("rating", 0))
        if isinstance(result, dict):
            score = result.get("trust_score")
            sentiment_score = result.get("sentiment_score")
            if isinstance(score, (int, float)):
                trust_scores.append(score)
            r["sentiment"] = sentiment_score if isinstance(sentiment_score, (int, float)) else "neutral"
            r["trust_score"] = score if isinstance(score, (int, float)) else 0
            r["topics"] = map_topics(r["comment"])
            r["spam"] = detect_spam(r["comment"])

    all_topics = []
    for t in texts:
        all_topics.extend(map_topics(t))

    risk = analyze_risk({
        "spam_count": spam_count,
        "total_reviews": len(reviews),
        "trust_scores": trust_scores,
        "sentiments": sentiments
    })

    persona_label, persona_tags = build_persona(
        emotion_avg, sentiments, all_topics, risk["risk_level"]
    )

    trust_score_final = round(sum(trust_scores) / len(trust_scores), 2) if trust_scores else 0
    top_topics = list(dict.fromkeys(all_topics))[:3]

    profile = {
        "user_id": user_id,
        "total_reviews": len(reviews),
        "average_rating": round(sum(ratings) / len(ratings), 2),
        "emotions": emotion_avg,
        "trust_scores": trust_scores,
        "trust_score": trust_score_final,
        "topics_most_common": top_topics,
        "risk": risk,
        "persona_label": persona_label,
        "persona_tags": persona_tags
    }

    profile["user_summary"] = generate_summary(profile)
    profile["insights"] = generate_insights(profile)

    return profile

def analyze_single_review(review):
    comment = review.get("comment", "")
    rating = review.get("rating", 0)

    sentiment_result = check_alignment(comment, rating)
    trust_score = 0
    sentiment = "neutral"
    if isinstance(sentiment_result, dict):
        trust_score = sentiment_result.get("trust_score", 0)
        sentiment = sentiment_result.get("sentiment_score", "neutral")

    topics = map_topics(comment)
    spam = detect_spam(comment)

    enriched_review = {
        **review,
        "sentiment": sentiment,
        "spam": spam,
        "topics": topics,
        "trust_score": trust_score
    }
    return enriched_review

def analyze_batch_and_generate_profiles(reviews_batch, db):
    for col in ["users", "products", "reviews", "user_evaluation"]:
        if col not in db.list_collection_names():
            db.create_collection(col)

    user_map = {}
    for review in reviews_batch:
        # Cadastro completo de usuários
        db["users"].update_one(
            {"user_id": review["user_id"]},
            {"$setOnInsert": {
                "user_id": review["user_id"],
                "name": review.get("user_name", "Unnamed User"),
                "email": review.get("user_email", "unknown@example.com")
            }},
            upsert=True
        )
        # Cadastro completo de produtos
        db["products"].update_one(
            {"product_id": review["product_id"]},
            {"$setOnInsert": {
                "product_id": review["product_id"],
                "name": review.get("product_name", "Unnamed Product"),
                "category": review.get("product_category", "uncategorized")
            }},
            upsert=True
        )

        user_map.setdefault(review["user_id"], []).append(review)

    enriched_reviews = []
    user_profiles = []

    for user_id, reviews in user_map.items():
        for review in reviews:
            enriched_review = analyze_single_review(review)
            enriched_reviews.append(enriched_review)

    if enriched_reviews:
        db["reviews"].insert_many(enriched_reviews)

    for user_id, reviews in user_map.items():
        profile = generate_profile(user_id, reviews)
        user_profiles.append(profile)
        db["user_evaluation"].update_one({"user_id": user_id}, {"$set": profile}, upsert=True)

    save_log(user_profiles)

def save_log(user_profiles):
    LOG_FOLDER = "C:/Users/mikam/OneDrive/Desktop/reviews_platform/logs/behavior_analysis"
    os.makedirs(LOG_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{LOG_FOLDER}/IA_log_{timestamp}.txt"

    persona_counter = {}
    risk_counter = {"low": 0, "medium": 0, "high": 0}
    total_users = len(user_profiles)

    for profile in user_profiles:
        persona = profile.get("persona_label", "unknown")
        risk = profile.get("risk", {}).get("risk_level", "unknown")
        persona_counter[persona] = persona_counter.get(persona, 0) + 1
        risk_counter[risk] = risk_counter.get(risk, 0) + 1

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"[AI LOG] Behavioral Analysis - {timestamp}\n\n")
        f.write(f"Users processed: {total_users}\n\n")
        f.write("Persona Distribution:\n")
        for persona, count in persona_counter.items():
            f.write(f" - {persona}: {count}\n")
        f.write("\nRisk Distribution:\n")
        for level, count in risk_counter.items():
            f.write(f" - {level.title()}: {count}\n")

def generate_summary(profile):
    persona = profile.get("persona_label", "undefined")
    emotions = profile.get("emotions", {})
    top_topics = profile.get("topics_most_common", [])
    risk = profile.get("risk", {}).get("risk_level", "unknown")
    avg_rating = profile.get("average_rating", 0)

    emotion_desc = {
        "happy": "positive and optimistic",
        "angry": "reactive and critical",
        "sad": "reflective and sensitive",
        "fear": "cautious and alert",
        "surprise": "spontaneous and responsive",
        "neutral": "neutral and objective"
    }

    mood = "neutral"
    if emotions:
        dominant_emotion = max(emotions, key=emotions.get)
        mood = emotion_desc.get(dominant_emotion, "neutral")

    if not top_topics:
        focus_area = "various subjects"
    else:
        focus_area = "topics such as " + ", ".join(top_topics)

    risk_phrase = {
        "low": "shows a stable behavioral pattern",
        "medium": "shows variations that may deserve attention",
        "high": "shows signs of volatile behavior"
    }.get(risk, "has an undefined behavioral pattern")

    summary = (
        f"With an average rating of {avg_rating}, this user demonstrates a {mood} profile, "
        f"with recurring focus on {focus_area}. Labeled as '{persona}', the user {risk_phrase}."
    )

    return summary

def generate_insights(profile):
    insights = []
    if profile.get("risk", {}).get("risk_level") == "low":
        insights.append("Consistent reviews with no risk detected")
    if profile.get("trust_score", 0) >= 80:
        insights.append("High reliability in reviews")
    if profile.get("emotions", {}).get("happy", 0) > 0.5:
        insights.append("Predominantly positive emotional tendency")
    if "entrega" in profile.get("topics_most_common", []):
        insights.append("Frequent focus on delivery issues")
    return insights
