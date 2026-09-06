"""
Example usage of Dynamic PDDL Domain Problem Parser Skill.
"""

from client import PDDLParser


def main():
    print("=== Dynamic PDDL Domain Problem Parser Demonstration ===")
    parser = PDDLParser()

    sample_domain = """
    (define (domain logistics-agent)
      (:predicates (at ?pkg ?loc) (vehicle_at ?v ?loc) (loaded ?pkg ?v))
      (:action load_package
        :parameters (?pkg ?v ?loc)
        :precondition (and (at ?pkg ?loc) (vehicle_at ?v ?loc))
        :effect (and (loaded ?pkg ?v) (not (at ?pkg ?loc)))
      )
      (:action unload_package
        :parameters (?pkg ?v ?loc)
        :precondition (and (loaded ?pkg ?v) (vehicle_at ?v ?loc))
        :effect (and (at ?pkg ?loc) (not (loaded ?pkg ?v)))
      )
    )
    """

    sample_problem = """
    (define (problem deliver-task-01)
      (:domain logistics-agent)
      (:objects pkg1 truck1 warehouse dock)
      (:init (at pkg1 warehouse) (vehicle_at truck1 warehouse))
      (:goal (at pkg1 dock))
    )
    """

    print("Parsing PDDL Domain...")
    domain_ast = parser.parse_domain(sample_domain)
    print(f"  Domain: {domain_ast['domain_name']} ({len(domain_ast['actions'])} actions)")
    for act in domain_ast["actions"]:
        print(f"    Action: {act['name']} | Params: {act['parameters']}")

    print("\nParsing PDDL Problem...")
    problem_ast = parser.parse_problem(sample_problem)
    print(f"  Problem: {problem_ast['problem_name']} | Domain Ref: {problem_ast['domain_name']}")
    print(f"  Objects: {problem_ast['objects']}")
    print(f"  Initial State: {problem_ast['init_predicates']}")
    print(f"  Goal: {problem_ast['goal']}")


if __name__ == "__main__":
    main()
