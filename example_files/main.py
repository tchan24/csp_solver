import sys

def read_file(file_name):
    with open(file_name, "r") as f:
        return f.read()

def parse_var(var_file):
    var_dict = {}
    lines = var_file.strip().split("\n")
    for line in lines:
        var, vals = line.split(":")
        var_dict[var.strip()] = list(map(int, vals.strip().split()))
    return var_dict

def parse_con(con_file):
    constraints = []
    lines = con_file.strip().split("\n")
    for line in lines:
        con = line.strip().split()
        if con[1] == "=":
            constraints.append((con[0], int(con[2]), "="))
        else:
            constraints.append((con[0], con[2], con[1]))
    return constraints

def forward_checking(var_dict, constraints, branches=None):
    if branches is None:
        branches = []
    if not var_dict:
        branches.append({})
        return branches
    var = min(var_dict, key=lambda x: len(var_dict[x]))
    for val in var_dict[var]:
        new_var_dict = var_dict.copy()
        new_var_dict.pop(var)
        new_branches = []
        for branch in branches:
            if is_consistent(var, val, branch, constraints):
                new_branch = branch.copy()
                new_branch[var] = val
                new_branches.append(new_branch)
        if new_branches:
            new_branches = forward_checking(new_var_dict, constraints, new_branches)
            branches += new_branches
    return branches

def is_consistent(var, val, branches, constraints):
    branch = {}
    for variable, value in branches.items():
        branch[variable] = value
    branch[var] = val
    for constraint in constraints:
        if constraint[0] == var and constraint[1] in branch and branch[constraint[1]] >= val:
            return False
    return True

if __name__ == "__main__":
    var_file = read_file(sys.argv[1])
    con_file = read_file(sys.argv[2])
    var_dict = parse_var(var_file)
    constraints = parse_con(con_file)
    branches = forward_checking(var_dict, constraints)
    for branch in branches:
        print(branch)
