from dso.tokenizer import tokenize
from dso.rules import REGISTER_RULES, DOMAIN_RULES
from dso.complexity import estimate_complexity, AGENT_MAP


def classify_register(tokens):
    best_register = "sense"
    best_count = 0
    for register, keywords in REGISTER_RULES.items():
        count = sum(1 for t in tokens if t in keywords)
        if count > best_count:
            best_count = count
            best_register = register
    total = len(tokens)
    confidence = best_count / total if total > 0 else 0.0
    return best_register, round(confidence, 4), best_count


def classify_domain(tokens):
    best_domain = "general"
    best_count = 0
    for domain, keywords in DOMAIN_RULES.items():
        count = sum(1 for t in tokens if t in keywords)
        if count > best_count:
            best_count = count
            best_domain = domain
    return best_domain, best_count


def route(task):
    if not task or not isinstance(task, str) or not task.strip():
        return {
            "register": "sense", "domain": "general",
            "complexity": "trivial", "suggested_agent": "sint-dso-agent",
            "confidence": 0.0, "reasoning": "empty input"
        }
    tokens = tokenize(task)
    register, reg_conf, reg_count = classify_register(tokens)
    domain, dom_count = classify_domain(tokens)
    complexity, _ = estimate_complexity(reg_count + dom_count, len(tokens))
    confidence = round((reg_conf + min(dom_count / max(len(tokens), 1), 1.0)) / 2, 4)
    return {
        "register": register,
        "domain": domain,
        "complexity": complexity,
        "suggested_agent": AGENT_MAP[complexity],
        "confidence": confidence,
        "reasoning": f"matched {reg_count} register + {dom_count} domain keywords"
    }
