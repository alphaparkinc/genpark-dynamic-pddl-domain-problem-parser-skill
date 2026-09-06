"""
MCP Server for Dynamic PDDL Domain Problem Parser Skill.
"""

import json
import sys
from client import PDDLParser

PARSER = PDDLParser()


def handle_request(req: dict) -> dict:
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "parse_domain",
                    "description": "Parse PDDL domain into JSON AST",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "domain_text": {"type": "string"}
                        },
                        "required": ["domain_text"]
                    }
                },
                {
                    "name": "parse_problem",
                    "description": "Parse PDDL problem definition into JSON AST",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "problem_text": {"type": "string"}
                        },
                        "required": ["problem_text"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "parse_domain":
            res = PARSER.parse_domain(args["domain_text"])
            return {"content": [{"type": "text", "text": json.dumps(res)}]}

        elif tool_name == "parse_problem":
            res = PARSER.parse_problem(args["problem_text"])
            return {"content": [{"type": "text", "text": json.dumps(res)}]}

        return {"error": f"Unknown tool: {tool_name}"}

    return {"error": f"Unknown method: {method}"}


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            resp["id"] = req.get("id")
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"error": str(e)}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
