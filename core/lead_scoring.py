def score_lead(data):
    score = 0
    if data["intent"] == "buy":
        score += 50
    if data["urgency"] == "high":
        score += 30
    return score
