# behavior_AI/04_risk_analyzer.py

def analyze_risk(user_metrics):
    """
    Recebe um dicionário com métricas do usuário e retorna avaliação de risco.
    Espera campos como:
      - spam_count
      - total_reviews
      - trust_scores (lista)
      - sentiments (lista: positive/neutral/negative)
    """
    risk_score = 0
    reasons = []

    # Heurística: muitos spams
    if user_metrics["spam_count"] / user_metrics["total_reviews"] > 0.4:
        risk_score += 2
        reasons.append("High spam ratio")

    # Heurística: baixa confiança geral
    if "trust_scores" in user_metrics:
        avg_trust = sum(user_metrics["trust_scores"]) / len(user_metrics["trust_scores"])
        if avg_trust < 60:
            risk_score += 2
            reasons.append(f"Low trust average ({avg_trust:.1f}%)")

    # Heurística: polaridade emocional extrema
    neg = user_metrics["sentiments"].count("negative")
    pos = user_metrics["sentiments"].count("positive")
    if abs(pos - neg) >= user_metrics["total_reviews"] * 0.6:
        risk_score += 1
        reasons.append("Emotionally polarized behavior")

    # Classificação final
    if risk_score >= 4:
        risk_level = "high"
    elif risk_score >= 2:
        risk_level = "moderate"
    else:
        risk_level = "low"

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "risk_reasons": reasons
    }

# Teste rápido
if __name__ == "__main__":
    example = {
        "spam_count": 5,
        "total_reviews": 10,
        "trust_scores": [50, 55, 45, 30, 65, 70],
        "sentiments": ["negative", "negative", "positive", "negative", "neutral", "positive", "positive", "positive", "positive", "positive"]
    }

    print(analyze_risk(example))
