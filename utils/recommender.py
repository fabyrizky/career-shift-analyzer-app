# utils/recommender.py

def simple_recommender(user_skills: list, interest_fields: list):
    job_mapping = {
        "Artificial Intelligence": {
            "skills": ["python", "machine learning", "data", "sql"],
            "jobs": ["Data Analyst", "AI Research Assistant", "Prompt Engineer"]
        },
        "Blockchain": {
            "skills": ["solidity", "crypto", "security", "smart contract"],
            "jobs": ["Blockchain Auditor", "Smart Contract Developer"]
        },
        "Renewable Energy": {
            "skills": ["solar", "electrical", "sustainability"],
            "jobs": ["Solar Energy Technician", "Green Finance Analyst"]
        },
        "Biotechnology": {
            "skills": ["biology", "genetics", "lab", "bioinformatics"],
            "jobs": ["Bioinformatics Analyst", "Lab Research Assistant"]
        },
        "Space Exploration": {
            "skills": ["physics", "engineering", "aerospace", "navigation"],
            "jobs": ["Aerospace Data Engineer", "Space Operations Analyst"]
        }
    }

    recommendations = {}

    for field in interest_fields:
        matched = any(skill.lower() in job_mapping[field]["skills"] for skill in user_skills)
        if matched:
            recommendations[field] = job_mapping[field]["jobs"]
        else:
            recommendations[field] = ["(Perlu pelatihan lebih lanjut - skill gap terdeteksi)"]

    return recommendations
