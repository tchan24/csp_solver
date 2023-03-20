import sys
from collections import defaultdict

def parse_var_file(filename):
    with open(filename, 'r') as f:
        return {name: (name, list(map(int, domain.strip().split()))) for line in f for name, domain in [line.strip().split(':')]}

def parse_con_file(filename):
    with open(filename, 'r') as f:
        return [tuple(line.strip().split()) for line in f]

def is_consistent(var, value, assignment, constraints):
    temp_assignment = assignment.copy()
    temp_assignment[var] = value

    for constraint in constraints:
        if constraint[0] == var:
            other = constraint[2]
            if other in temp_assignment:
                if not eval(f"{temp_assignment[var]} {constraint[1]} {temp_assignment[other]}"):
                    return False
        elif constraint[2] == var:
            other = constraint[0]
            if other in temp_assignment:
                if not eval(f"{temp_assignment[other]} {constraint[1]} {temp_assignment[var]}"):
                    return False

    return True

def most_constrained_variable(unassigned, constraints):
    return min(unassigned, key=lambda x: (-sum(x in (var1, var2) for var1, _, var2 in constraints), x))

def least_constraining_value(var, assignment, constraints):
    return sorted(var[1], key=lambda x: (sum(is_consistent(var[0], x, assignment, constraints) for var1, _, var2 in constraints for other_var in [var1 if var2 == var[0] else var2] if other_var not in assignment), x))

def backtrack(assignment, variables, constraints, consistency):
    if len(assignment) == len(variables):
        return assignment, []

    branches = []
    unassigned = [var for var in variables if var not in assignment]
    var = variables[most_constrained_variable(unassigned, constraints)]

    for value in least_constraining_value(var, assignment, constraints):
        if consistency == 'none' or is_consistent(var[0], value, assignment, constraints):
            assignment[var[0]] = value
            temp_assignment = assignment.copy()
            result, new_branches = backtrack(temp_assignment, variables, constraints, consistency)
            branches.extend([(var[0], value)] + branch for branch in new_branches)
            if result:
                return result, branches
            del assignment[var[0]]

    return None, branches

def main():
    var_filename, con_filename, consistency = sys.argv[1:4]

    variables = parse_var_file(var_filename)
    constraints = parse_con_file(con_filename)

    print(f"Variables: {variables}")
    print(f"Constraints: {constraints}")

    solution, branches = backtrack({}, variables, constraints, consistency)

    if solution:
        assignment_str = ', '.join(f"{var} = {value}" for var, value in solution.items())
        print(f"Solution: {assignment_str}")
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
