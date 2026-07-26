import json
import os

from config import RULES_PATH, DEFAULT_RULES_PATH

# built-in register rules
REGISTER_RULES = {
    "sense":   {"observe", "see", "read", "look", "data", "output", "log", "trace",
                "sense", "perceive", "detect", "monitor", "capture"},
    "fact":    {"verify", "check", "confirm", "what", "fact", "source", "document",
                "rfc", "spec", "documentation", "evidence", "cite", "reference"},
    "logic":   {"why", "because", "infer", "deduce", "conclude", "imply", "therefore",
                "reason", "analysis", "analytic", "logical", "if", "then"},
    "opinion": {"think", "believe", "prefer", "suggest", "recommend", "maybe",
                "probably", "opinion", "feel", "guess", "suppose"},
    "action":  {"do", "make", "create", "build", "write", "implement", "fix",
                "change", "add", "delete", "remove", "update", "modify"},
    "causality": {"cause", "lead", "result", "trigger", "affect", "influence",
                  "impact", "depend", "condition", "consequence"},
}

DOMAIN_RULES = {
    "ada-spark": {"ada", "spark", "gnatprove", "ada2012", "ravenscar"},
    "reverse":   {"binary", "elf", "pe", "reverse", "disassem", "decompile",
                  "revers", "ghidra", "ida", "radare", "objdump"},
    "crypto":    {"crypto", "aes", "cipher", "s-box", "encrypt", "decrypt",
                  "key", "hash", "sha", "md5", "plaintext", "ciphertext"},
    "embed":     {"embedded", "mcu", "rtos", "linker", "firmware", "bare-metal",
                  "gpio", "spi", "i2c", "uart", "interrupt"},
    "dsa":       {"audio", "dsp", "mixer", "sample", "filter", "fft", "signal",
                  "waveform", "sound"},
    "code":      {"code", "implement", "write", "function", "class", "method",
                  "module", "library", "api", "syntax", "compil"},
    "memory":    {"memory", "block", "chain", "allocat", "heap", "stack",
                  "arena", "pool", "fragment", "garbage"},
    "data":      {"data", "parse", "transform", "json", "csv", "xml", "schema",
                  "dataset", "pipeline", "etl"},
    "systems":   {"system", "kernel", "driver", "syscall", "module", "interrupt",
                  "mmu", "page", "scheduler", "process", "thread"},
}

LEARNED_RULES = {"register": {}, "domain": {}}


def load_rules(path=None):
    p = path or os.path.expanduser(RULES_PATH or DEFAULT_RULES_PATH)
    try:
        with open(p) as f:
            rules = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return
    for reg, kws in rules.get("register", {}).items():
        if reg in REGISTER_RULES:
            REGISTER_RULES[reg].update(kws)
        else:
            REGISTER_RULES[reg] = set(kws)
    for dom, kws in rules.get("domain", {}).items():
        if dom in DOMAIN_RULES:
            DOMAIN_RULES[dom].update(kws)
        else:
            DOMAIN_RULES[dom] = set(kws)


def save_rules(path=None):
    p = path or os.path.expanduser(RULES_PATH or DEFAULT_RULES_PATH)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    data = {
        "register": {k: list(v) for k, v in REGISTER_RULES.items()},
        "domain":   {k: list(v) for k, v in DOMAIN_RULES.items()},
    }
    with open(p, "w") as f:
        json.dump(data, f, indent=2)


def learn_register(register, keywords):
    if register not in REGISTER_RULES:
        REGISTER_RULES[register] = set()
    REGISTER_RULES[register].update(keywords)
    save_rules()


def learn_domain(domain, keywords):
    if domain not in DOMAIN_RULES:
        DOMAIN_RULES[domain] = set()
    DOMAIN_RULES[domain].update(keywords)
    save_rules()
