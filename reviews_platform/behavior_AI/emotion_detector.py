# behavior_AI/emotion_detector.py

from transformers import pipeline
from collections import defaultdict

# Baixe o modelo da primeira vez; depois fica offline
emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None
)

def detect_emotions(texts):
    """
    Retorna a média das emoções detectadas para uma lista de textos.
    Compatível com diferentes estruturas de retorno do Hugging Face.
    """
    emotion_totals = defaultdict(float)
    total_valid = 0

    for text in texts:
        try:
            result = emotion_classifier(text)
            # Corrige se resultado vier como lista de listas (pode acontecer!)
            if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
                result = result[0]
            for item in result:
                emotion = item['label'].lower()
                score = float(item['score'])
                emotion_totals[emotion] += score
            total_valid += 1
        except Exception as e:
            print(f"[WARNING] Erro ao analisar emoção: {e}")
            continue

    if total_valid == 0:
        # Emotions possíveis do modelo
        return {k: 0.0 for k in ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]}

    emotion_avg = {k: round(emotion_totals[k] / total_valid, 3) for k in emotion_totals}
    return emotion_avg

# Teste rápido
if __name__ == "__main__":
    print(detect_emotions([
        "I love this product! It made my day.",
        "This is so frustrating and I hate it.",
        "It is okay, nothing special.",
    ]))
