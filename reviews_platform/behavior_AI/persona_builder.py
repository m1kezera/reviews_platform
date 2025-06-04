# behavior_AI/05_persona_builder.py

def build_persona(emotions, sentiments, top_topics, risk_level):
    """
    Gera um rótulo descritivo de persona baseado em padrões emocionais e de comportamento.
    Params:
      - emotions: dict com % de emoções (happy, sad, etc.)
      - sentiments: lista de 'positive', 'neutral', 'negative'
      - top_topics: lista com os 3 tópicos mais frequentes
      - risk_level: 'low', 'moderate', 'high'
    Returns:
      - persona_label (str)
      - behavioral_tags (list of str)
    """
    tags = []

    # Emoções dominantes
    if emotions:
        top_emotion = max(emotions, key=emotions.get)
        emotion_map = {
            "happy": "optimistic",
            "sad": "reflective",
            "angry": "demanding",
            "fear": "cautious",
            "surprise": "reactive"
        }
        tags.append(emotion_map.get(top_emotion, "neutral"))

    # Sentimento geral
    pos = sentiments.count("positive")
    neg = sentiments.count("negative")
    neu = sentiments.count("neutral")
    if pos > neg and pos > neu:
        tags.append("satisfied")
    elif neg > pos:
        tags.append("critical")
    elif neu > pos and neu > neg:
        tags.append("reserved")

    # Interesse dominante
    if top_topics:
        topic_map = {
            "delivery": "impatient",
            "product_quality": "detailed",
            "performance": "technical",
            "sound": "sensitive",
            "customer_service": "demanding",
            "price": "value-seeker",
            "design": "aesthetic"
        }
        for t in top_topics[:2]:
            if t in topic_map:
                tags.append(topic_map[t])

    # Risco
    if risk_level == "high":
        tags.append("unpredictable")
    elif risk_level == "moderate":
        tags.append("unstable")
    else:
        tags.append("stable")

    # Construção final
    unique_tags = list(dict.fromkeys(tags))  # remove duplicados mantendo ordem
    persona_label = ", ".join(unique_tags).capitalize()

    return persona_label, unique_tags

# Teste rápido
if __name__ == "__main__":
    emotions = {"happy": 50.0, "angry": 20.0, "sad": 10.0, "fear": 10.0, "surprise": 10.0}
    sentiments = ["positive", "positive", "neutral", "negative", "positive", "neutral"]
    topics = ["design", "product_quality", "price"]
    risk = "moderate"

    label, tags = build_persona(emotions, sentiments, topics, risk)
    print("Persona Label:", label)
    print("Tags:", tags)
