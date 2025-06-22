# utils/future_readiness.py

def calculate_readiness_score(user_skills, interest_fields, waktu_belajar):
    base_weights = {
        "Artificial Intelligence": ["python", "sql", "machine learning"],
        "Blockchain": ["crypto", "solidity", "smart contract"],
        "Renewable Energy": ["solar", "sustainability", "electrical"],
        "Biotechnology": ["bioinformatics", "genetics", "lab"],
        "Space Exploration": ["physics", "engineering", "navigation"]
    }

    matched_skills = 0
    total_required = 0

    for field in interest_fields:
        required = base_weights.get(field, [])
        total_required += len(required)
        for skill in user_skills:
            if skill in required:
                matched_skills += 1

    # Skor dasar dari kecocokan skill
    if total_required == 0:
        skill_score = 0
    else:
        skill_score = matched_skills / total_required

    # Skor tambahan dari waktu belajar (semakin tinggi semakin siap)
    belajar_boost = min(waktu_belajar / 20, 1.0)

    total_score = round((0.7 * skill_score + 0.3 * belajar_boost) * 100)

    return total_score
