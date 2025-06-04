# behavior_AI/03_topic_mapper.py

from collections import Counter

# Palavras-chave por tópico
topic_keywords = {
    "delivery": ["late", "arrived", "fast", "shipping", "delayed", "on time"],
    "product_quality": ["broken", "defective", "perfect", "bad", "quality", "durable", "cheap"],
    "sound": ["sound", "audio", "volume", "noise", "music", "clarity"],
    "performance": ["slow", "fast", "lag", "crash", "smooth", "performance"],
    "customer_service": ["support", "rude", "helpful", "service", "contact"],
    "price": ["cheap", "expensive", "worth", "value", "deal", "price"],
    "design": ["design", "beautiful", "ugly", "colors", "style", "look"]
}

def map_topics(text):
    """
    Mapeia um comentário para os tópicos mais prováveis com base em palavras-chave.
    Retorna lista de tópicos encontrados ou ["general"] se nenhum for detectado.
    """
    text = text.lower()
    matched = []

    for topic, keywords in topic_keywords.items():
        if any(kw in text for kw in keywords):
            matched.append(topic)

    return matched if matched else ["general"]

def top_topics(comments, top_n=3):
    """
    Recebe uma lista de comentários e retorna os tópicos mais mencionados.
    """
    topic_list = []
    for comment in comments:
        topic_list.extend(map_topics(comment))

    count = Counter(topic_list)
    return [t for t, _ in count.most_common(top_n)]

# Teste rápido
if __name__ == "__main__":
    example = [
        "The shipping was super fast!",
        "Terrible sound quality, lots of noise.",
        "I loved the design, looks amazing.",
        "Customer support was helpful and quick.",
        "It's worth the price."
    ]
    for c in example:
        print(c, "→", map_topics(c))

    print("\nTop topics:", top_topics(example))
