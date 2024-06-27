from pyomo.environ import *
import random
print('stress test')
random.seed(5)

# Create a Concrete Model
model = ConcreteModel()

# Sets
# set of All nodes in the supply chain
i = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P12', 'P13', 'P14', 'P15', 'P16', 'P17',
     'P18', 'P19', 'P20']

# set of relationship between nodes
j = [('P1', 'P9'), ('P1', 'P19'), ('P2', 'P9'), ('P2', 'P15'), ('P2', 'P20'), ('P3', 'P10'), ('P3', 'P16'),
     ('P4', 'P11'), ('P5', 'P11'),
     ('P6', 'P11'), ('P6', 'P17'), ('P7', 'P12'), ('P7', 'P13'), ('P7', 'P14'), ('P7', 'P18'), ('P8', 'P13'),
     ('P9', 'P14'), ('P9', 'P19'),
     ('P10', 'P14'), ('P10', 'P15'), ('P10', 'P20'), ('P11', 'P14'), ('P11', 'P16'), ('P12', 'P15'), ('P12', 'P16'),
     ('P12', 'P17'),
     ('P13', 'P17'), ('P13', 'P18'), ('P14', 'P18'), ('P15', 'P18'), ('P15', 'P19'), ('P16', 'P19'), ('P16', 'P20'),
     ('P17', 'P20')]

# BOM relationship
r = {('P1', 'P9'): 4, ('P1', 'P19'): 11, ('P2', 'P9'): 2, ('P2', 'P15'): 8, ('P2', 'P20'): 16, ('P3', 'P10'): 4,
     ('P3', 'P16'): 6, ('P4', 'P11'): 2, ('P5', 'P11'): 3,
     ('P6', 'P11'): 2, ('P6', 'P17'): 12, ('P7', 'P12'): 1, ('P7', 'P13'): 1, ('P7', 'P14'): 5, ('P7', 'P18'): 15,
     ('P8', 'P13'): 4, ('P9', 'P14'): 1, ('P9', 'P19'): 3,
     ('P10', 'P14'): 1, ('P10', 'P15'): 2, ('P10', 'P20'): 4, ('P11', 'P14'): 1, ('P11', 'P16'): 1, ('P12', 'P15'): 2,
     ('P12', 'P16'): 1, ('P12', 'P17'): 3,
     ('P13', 'P17'): 4, ('P13', 'P18'): 10, ('P14', 'P18'): 2, ('P15', 'P18'): 1, ('P15', 'P19'): 1, ('P16', 'P19'): 2,
     ('P16', 'P20'): 1, ('P17', 'P20'): 2}

# set of final products
k = ['P18', 'P19', 'P20']

# Parameters
demand = {'P18': 500, 'P19': 400, 'P20': 600}

# parameters-capacity
capacity = {i1: random.randint(5000, 10000) for i1 in i}

# parameters-Initial Inventory
Inventory = {i1: random.randint(1500, 7000) for i1 in i}

# Variables
model.u = Var(i, domain=NonNegativeReals)
model.y = Var(j, domain=NonNegativeReals)
model.t = Var(domain=NonNegativeReals)

# Objective function

Obj = model.t
model.obj = Objective(expr=Obj, sense=maximize)

# constraints
model.Constraints = ConstraintList()

# BOM constraints
for (comp, prod), qty in r.items():
    model.Constraints.add(model.u[prod] * qty <= model.y[(comp, prod)])

# production and inventory
# Extract unique upstream_nodes
upstream_node = list(set(i1 for i1, _ in j))

for i1 in upstream_node:
    model.Constraints.add(sum(model.y[(i1, j1)] for (i1_tmp, j1) in j if i1_tmp == i1) <= model.u[i1] + Inventory[i1])

# ِDemand satisfying with no shortage
for i1 in k:
    model.Constraints.add(model.u[i1] + Inventory[i1] >= demand[i1] * model.t)

# Capacity constraint
for i1 in i:
    model.Constraints.add(model.u[i1] <= capacity[i1] * model.t)

# solver
solver = SolverFactory('glpk')
obj_values = []

for i1 in i:
    disruption_constraint = model.Constraints.add(model.u[i1] <= 0)

    results = solver.solve(model)

    # Store the objective value
    obj_values.append(value(model.obj))
    if (results.solver.status == SolverStatus.ok) and (
            results.solver.termination_condition == TerminationCondition.optimal):
        # Print the result for each element
        print(f"i1: {i1}, TTS: {value(model.obj)}")

    # remove disruption constrain for the current iteration
    disruption_constraint.deactivate()
