# behavior_AI/02_sentiment_tuner.py

from transformers import pipeline

# Pipeline do Hugging Face
sentiment_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def get_sentiment_score(text):
    """
    Converte a saída textual da IA (1 to 5 stars) em um score de -1 (negativo) a +1 (positivo).
    """
    try:
        result = sentiment_model(text)[0]
        label = result["label"]
        stars = int(label.split()[0])  # extrai "1", "2", ..., "5"
        # Mapeia: 1→-1.0, 3→0.0, 5→+1.0
        score = round((stars - 3) / 2, 2)
        return score
    except Exception as e:
        return {"error": str(e)}

def check_alignment(text, given_rating):
    """
    Avalia a coerência entre sentimento textual e nota dada.
    Retorna o score calculado, a diferença e um trust score de 0 a 100.
    """
    score = get_sentiment_score(text)
    if isinstance(score, dict) and "error" in score:
        return score

    norm_rating = round((given_rating - 3) / 2, 2)  # também -1 a +1
    diff = round(abs(score - norm_rating), 2)
    trust = max(0, round((1 - diff) * 100, 1))  # quanto menor a diferença, maior o trust

    return {
        "sentiment_score": score,
        "expected_from_rating": norm_rating,
        "coherence_diff": diff,
        "trust_score": trust
    }

# Teste rápido
if __name__ == "__main__":
    sample_text = "This product is amazing and exceeded all my expectations!"
    given_rating = 5
    print(check_alignment(sample_text, given_rating))
