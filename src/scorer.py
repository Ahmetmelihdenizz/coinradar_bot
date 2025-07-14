ML_WEIGHT = 0.65
TECH_WEIGHT = 0.35

def compute_score(probability: float, technical_score: float = 50) -> float:
    return round(
        technical_score * TECH_WEIGHT +
        probability * 100 * ML_WEIGHT,
        2
    )

if __name__ == "__main__":
    prob = 0.0715
    tech = 70
    skor = compute_score(prob, tech)
    print(f"Örnek skor: {skor}")
