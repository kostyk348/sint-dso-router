import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    FastMCP = None

from dso.classifier import route
from dso.rules import REGISTER_RULES, DOMAIN_RULES, learn_register, learn_domain, load_rules
from config import NAME, VERSION

load_rules()

if FastMCP is None:
    mcp = None
else:
    mcp = FastMCP(NAME)


def _route_handler(task):
    return route(task)


def _register_stats():
    return {
        "version": VERSION,
        "registers": {
            k: sorted(v) for k, v in REGISTER_RULES.items()
        }
    }


def _domain_stats():
    return {
        "version": VERSION,
        "domains": {
            k: sorted(v) for k, v in DOMAIN_RULES.items()
        }
    }


def _learn_rule(register=None, keywords=None, domain=None):
    if not keywords:
        return {"error": "keywords required"}
    if register:
        learn_register(register, keywords)
        return {"status": "ok", "register": register, "keywords_added": len(keywords)}
    if domain:
        learn_domain(domain, keywords)
        return {"status": "ok", "domain": domain, "keywords_added": len(keywords)}
    return {"error": "register or domain required"}


def _test(task, expected_register, expected_domain):
    result = route(task)
    return {
        "task": task,
        "expected_register": expected_register,
        "expected_domain": expected_domain,
        "actual_register": result["register"],
        "actual_domain": result["domain"],
        "register_match": result["register"] == expected_register,
        "domain_match": result["domain"] == expected_domain,
        "all_match": result["register"] == expected_register and result["domain"] == expected_domain,
        "result": result,
    }


if mcp is not None:
    @mcp.tool()
    def dso_route(task: str) -> dict:
        return _route_handler(task)

    @mcp.tool()
    def dso_register_stats() -> dict:
        return _register_stats()

    @mcp.tool()
    def dso_domain_stats() -> dict:
        return _domain_stats()

    @mcp.tool()
    def dso_learn_rule(register: str = None, keywords: list = None, domain: str = None) -> dict:
        return _learn_rule(register, keywords, domain)

    @mcp.tool()
    def dso_test(task: str, expected_register: str, expected_domain: str) -> dict:
        return _test(task, expected_register, expected_domain)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="DSO Deterministic Router")
    parser.add_argument("--tool", choices=["route", "register-stats", "domain-stats",
                                           "learn-rule", "test"])
    parser.add_argument("--task")
    parser.add_argument("--expected-register")
    parser.add_argument("--expected-domain")
    parser.add_argument("--register")
    parser.add_argument("--domain")
    parser.add_argument("--keywords", nargs="+")
    args = parser.parse_args()

    if args.tool == "route":
        print(_route_handler(args.task))
    elif args.tool == "register-stats":
        print(_register_stats())
    elif args.tool == "domain-stats":
        print(_domain_stats())
    elif args.tool == "learn-rule":
        print(_learn_rule(args.register, args.keywords, args.domain))
    elif args.tool == "test":
        print(_test(args.task, args.expected_register, args.expected_domain))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
