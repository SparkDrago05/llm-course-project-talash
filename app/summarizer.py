from typing import Any


def build_candidate_summary(
    candidate_name: str,
    education_analysis: dict[str, Any],
    experience_analysis: dict[str, Any],
    missing_info: list[str],
) -> str:
    strength = education_analysis.get("strength_classification", "Unknown")
    progression = education_analysis.get("progression_summary", "No progression found")
    avg_score = education_analysis.get("average_score", 0)

    experience_years = experience_analysis.get("experience_duration_years", 0)
    career_progression = experience_analysis.get("career_progression", "undetermined")

    issues = []
    if education_analysis.get("gap_duration"):
        issues.append("educational gaps")
    if experience_analysis.get("flags"):
        issues.extend(experience_analysis.get("flags", []))
    if missing_info:
        issues.append("missing profile details")

    issues_text = ", ".join(issues) if issues else "no major timeline issues detected"

    if strength == "Strong" and experience_years >= 2:
        suitability = "Good fit"
    elif strength == "Weak":
        suitability = "Needs further review"
    else:
        suitability = "Moderate fit"

    return (
        f"{candidate_name}: Academic strength is {strength} (avg score {avg_score}%) with progression "
        f"[{progression}]. Professional experience is {experience_years} years with career trend "
        f"'{career_progression}'. Key observations: {issues_text}. Overall suitability: {suitability}."
    )
