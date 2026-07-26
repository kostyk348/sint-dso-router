def estimate_complexity(matched_count, domain_count):
    if matched_count < 2:
        return "trivial", 0.95
    if matched_count <= 4:
        return "simple", 0.85
    if matched_count <= 8:
        return "moderate", 0.75
    return "complex", 0.60


AGENT_MAP = {
    "trivial":  "sint-dso-agent",
    "simple":   "sint-lang-agent",
    "moderate": "sint-adv-agent",
    "complex":  "sint-expert-agent",
}
