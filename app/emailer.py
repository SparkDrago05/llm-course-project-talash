def build_missing_info_email(candidate_name: str, missing_fields: list[str]) -> str:
    greeting_name = candidate_name if candidate_name else "Candidate"

    if not missing_fields:
        return (
            f"Dear {greeting_name},\n\n"
            "Thank you for your CV submission. At this time, no additional information is required.\n\n"
            "Best regards,\n"
            "Recruitment Team\n"
            "TALASH"
        )

    bullet_lines = "\n".join(f"- {field}" for field in missing_fields)

    return (
        f"Dear {greeting_name},\n\n"
        "Thank you for your application and interest in the position. "
        "During our profile review, we noticed a few details are missing or unclear in your CV:\n\n"
        f"{bullet_lines}\n\n"
        "Please share an updated CV (PDF) with the above details so we can complete your assessment.\n"
        "If any item is not applicable, kindly mention that explicitly in your response.\n\n"
        "Best regards,\n"
        "Recruitment Team\n"
        "TALASH"
    )
