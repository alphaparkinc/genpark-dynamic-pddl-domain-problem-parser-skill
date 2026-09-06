"""
Dynamic PDDL Domain Problem Parser Skill Client
Pure Python Standard Library implementation of a PDDL (Planning Domain Definition Language) AST parser.
Tokenizes Lisp-like S-expressions and constructs structured domain schemas, action parameters,
preconditions, and problem goal specifications.
"""

import re
from typing import List, Dict, Any, Tuple, Optional


class PDDLParser:
    """
    Parses PDDL domain and problem specifications into Python dictionary ASTs.
    """

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """Convert PDDL text into S-expression token stream, stripping comments."""
        no_comments = re.sub(r';.*$', '', text, flags=re.MULTILINE)
        tokens = re.findall(r'\(|\)|[^\s()]+', no_comments)
        return tokens

    @staticmethod
    def _parse_s_expr(tokens: List[str]) -> Any:
        """Parse token stream into nested list S-expression."""
        if not tokens:
            return []
        token = tokens.pop(0)
        if token == '(':
            lst = []
            while tokens and tokens[0] != ')':
                lst.append(PDDLParser._parse_s_expr(tokens))
            if tokens and tokens[0] == ')':
                tokens.pop(0)
            return lst
        elif token == ')':
            raise ValueError("Unexpected ')'")
        else:
            return token

    def parse_domain(self, domain_text: str) -> Dict[str, Any]:
        """Parse PDDL domain definition."""
        tokens = self._tokenize(domain_text)
        s_expr = self._parse_s_expr(tokens)

        if not s_expr or s_expr[0] != "define" or s_expr[1][0] != "domain":
            raise ValueError("Invalid PDDL domain structure")

        domain_name = s_expr[1][1]
        actions = []
        predicates = []

        for item in s_expr[2:]:
            if item[0] == ":predicates":
                predicates = item[1:]
            elif item[0] == ":action":
                act_name = item[1]
                params = []
                prec = []
                effect = []

                i = 2
                while i < len(item):
                    if item[i] == ":parameters":
                        params = item[i + 1]
                        i += 2
                    elif item[i] == ":precondition":
                        prec = item[i + 1]
                        i += 2
                    elif item[i] == ":effect":
                        effect = item[i + 1]
                        i += 2
                    else:
                        i += 1

                actions.append({
                    "name": act_name,
                    "parameters": params,
                    "preconditions": prec,
                    "effects": effect
                })

        return {
            "domain_name": domain_name,
            "predicates_count": len(predicates),
            "actions": actions
        }

    def parse_problem(self, problem_text: str) -> Dict[str, Any]:
        """Parse PDDL problem definition."""
        tokens = self._tokenize(problem_text)
        s_expr = self._parse_s_expr(tokens)

        if not s_expr or s_expr[0] != "define" or s_expr[1][0] != "problem":
            raise ValueError("Invalid PDDL problem structure")

        problem_name = s_expr[1][1]
        domain_ref = ""
        objects = []
        init_state = []
        goal_state = []

        for item in s_expr[2:]:
            if item[0] == ":domain":
                domain_ref = item[1]
            elif item[0] == ":objects":
                objects = item[1:]
            elif item[0] == ":init":
                init_state = item[1:]
            elif item[0] == ":goal":
                goal_state = item[1]

        return {
            "problem_name": problem_name,
            "domain_name": domain_ref,
            "objects": objects,
            "init_predicates": init_state,
            "goal": goal_state
        }
