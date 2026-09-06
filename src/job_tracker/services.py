import re
from collections import Counter

SKILLS = {
    "python",
    "fastapi",
    "django",
    "flask",
    "sql",
    "postgresql",
    "docker",
    "kubernetes",
    "git",
    "linux",
    "aws",
    "azure",
    "pandas",
    "airflow",
    "spark",
    "machine learning",
    "pytorch",
    "tensorflow",
    "opencv",
    "rest",
    "ci/cd",
    "pytest",
    "redis",
    "rabbitmq",
    "microservices",
}


def extract_skills(text: str) -> set[str]:
    normalized = re.sub(r"[^a-z0-9+#/. -]", " ", text.lower())
    return {skill for skill in SKILLS if re.search(rf"(?<!\w){re.escape(skill)}(?!\w)", normalized)}


def analyze_match(resume: str, description: str) -> dict:
    resume_skills, required = extract_skills(resume), extract_skills(description)
    matched = sorted(resume_skills & required)
    missing = sorted(required - resume_skills)
    score = round(100 * len(matched) / len(required), 1) if required else 0.0
    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "method": "deterministic-v1",
    }


def stage_statistics(stages: list[str]) -> dict[str, int]:
    counts = Counter(stages)
    return {
        stage: counts.get(stage, 0)
        for stage in ["Saved", "Applied", "Interview", "Offer", "Rejected"]
    }
