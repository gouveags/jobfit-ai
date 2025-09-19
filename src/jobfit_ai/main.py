import numpy as np
from jobfit_ai.models import ComparisonScores


def evaluate_fit(scores: ComparisonScores, threshold: float = 0.65) -> dict:
    weights = np.array(
        [
            0.35,
            0.20,
            0.20,
            0.10,
            0.05,
            0.10,
        ]
    )

    score_values = np.array(
        [
            scores.technical_skills_score,
            scores.experience_years_score,
            scores.responsibilities_alignment_score,
            scores.education_score,
            scores.location_fit_score,
            scores.overall_softskills_score,
        ]
    )

    total = np.dot(score_values, weights)

    return {"fit": total >= threshold, "score": round(float(total), 3)}
