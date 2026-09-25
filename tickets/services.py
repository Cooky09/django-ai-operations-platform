def classify_ticket(title: str, description: str) -> tuple[str, str]:
    text = f"{title} {description}".lower()

    if any(word in text for word in ("login", "password", "account")):
        category = "authentication"
    elif any(word in text for word in ("payment", "invoice", "refund", "charge")):
        category = "billing"
    elif any(word in text for word in ("error", "crash", "bug", "exception")):
        category = "technical"
    else:
        category = "general"

    summary = description.strip().replace("\n", " ")
    if len(summary) > 180:
        summary = summary[:177] + "..."

    return category, summary
