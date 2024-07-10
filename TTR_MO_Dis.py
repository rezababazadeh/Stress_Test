from pyomo.environ import *
import random
import pandas as pd

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
     ('P3', 'P16'): 6, ('P4', 'P11'): 2,
     ('P5', 'P11'): 3, ('P6', 'P11'): 2, ('P6', 'P17'): 12, ('P7', 'P12'): 1, ('P7', 'P13'): 1, ('P7', 'P14'): 5,
     ('P7', 'P18'): 15, ('P8', 'P13'): 4,
     ('P9', 'P14'): 1, ('P9', 'P19'): 3, ('P10', 'P14'): 1, ('P10', 'P15'): 2, ('P10', 'P20'): 4, ('P11', 'P14'): 1,
     ('P11', 'P16'): 1,
     ('P12', 'P15'): 2, ('P12', 'P16'): 1, ('P12', 'P17'): 3, ('P13', 'P17'): 4, ('P13', 'P18'): 10, ('P14', 'P18'): 2,
     ('P15', 'P18'): 1,
     ('P15', 'P19'): 1, ('P16', 'P19'): 2, ('P16', 'P20'): 1, ('P17', 'P20'): 2}

# set of final products
k = ['P18', 'P19', 'P20']

# Parameters
demand = {'P18': 500, 'P19': 400, 'P20': 600}
# parameters-capacity
capacity = {i1: random.randint(5000, 15000) for i1 in i}

# parameters-Initial Inventory
Inventory = {i1: random.randint(100, 200) for i1 in i}

# parameters-Time to recover
TTR = {i1: random.randint(4, 10) for i1 in i}

# parameters-profit margin
f = {i1: random.randint(400, 800) for i1 in k}

# parameters-GHG at each node
GHG = {i1: random.randint(20, 35) for i1 in i}

# parameters-GHG1 in flow between nodes
GHG1 = {pair: random.randint(5, 15) for pair in j}

# parameters-Societal impact of each node
SI = {i1: random.randint(1, 10) for i1 in i}

# Variables
model.u = Var(i, domain=NonNegativeReals)
model.y = Var(j, domain=NonNegativeReals)
model.l = Var(k, domain=NonNegativeReals)

# Objective functions
Obj1 = sum(f[i1] * model.l[i1] for i1 in k)
model.obj1 = Objective(expr=Obj1, sense=minimize)

Obj2 = sum(GHG[i1] * model.u[i1] for i1 in i) + sum(gh * model.y[(i1, j1)] for (i1, j1), gh in GHG1.items())
model.obj2 = Objective(expr=Obj2, sense=minimize)

Obj3 = sum(SI[i1] * model.u[i1] for i1 in i)
model.obj3 = Objective(expr=Obj3, sense=maximize)

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
    model.Constraints.add(model.l[i1] + model.u[i1] + Inventory[i1] >= demand[i1] * TTR[i1])

# ِUpper bound for lost sales
for i1 in k:
    model.Constraints.add(model.l[i1] <= demand[i1] * TTR[i1])

# Capacity constraint
for i1 in i:
    model.Constraints.add(model.u[i1] <= capacity[i1] * TTR[i1])

# solver
solver = SolverFactory('cbc')

# Disruption scenarios
disruption_constraint = model.Constraints.add(model.u['P5'] <= 0)

# Step 1: Optimize the first objective
model.obj2.deactivate()
model.obj3.deactivate()
results = solver.solve(model, tee=True)
# Check the status of the model
if (results.solver.status == SolverStatus.ok) and (
        results.solver.termination_condition == TerminationCondition.optimal):
    print("The model was solved to optimality.")
elif results.solver.termination_condition == TerminationCondition.infeasible:
    print("The model is infeasible.")
else:
    print(f"Solver Status: {results.solver.status}")
    print(f"Termination Condition: {results.solver.termination_condition}")
# Print the objective function value if solved optimally
if results.solver.status == SolverStatus.ok and results.solver.termination_condition == TerminationCondition.optimal:
    print(f"Objective function value_1: {value(model.obj1)}")
model.display()
opt_value_obj1 = model.obj1()

# Step 2: Optimize the second objective
#Fixing optimal value for the first objective function
model.Constraints.add(sum(f[i1] * model.l[i1] for i1 in k)  <= opt_value_obj1+0.1)
model.obj2.activate()
model.obj1.deactivate()
results = solver.solve(model, tee=True)
# Check the status of the model
if (results.solver.status == SolverStatus.ok) and (
    results.solver.termination_condition == TerminationCondition.optimal):
    print("The model was solved to optimality.")
elif results.solver.termination_condition == TerminationCondition.infeasible:
    print("The model is infeasible.")
else:
    print(f"Solver Status: {results.solver.status}")
    print(f"Termination Condition: {results.solver.termination_condition}")
# Print the objective function value if solved optimally
if results.solver.status == SolverStatus.ok and results.solver.termination_condition == TerminationCondition.optimal:
    print(f"Objective function value_2: {value(model.obj2)}")
model.display()
opt_value_obj2 = model.obj2()

#  Step 3: Optimize the third objective
# Fixing optimal value for the second objective function
model.Constraints.add((sum(GHG[i1] * model.u[i1] for i1 in i) + sum(gh * model.y[(i1, j1)] for (i1, j1), gh in GHG1.items()))  <= opt_value_obj2+0.1)
model.obj3.activate()
model.obj2.deactivate()
results = solver.solve(model, tee=True)
# Check the status of the model
if (results.solver.status == SolverStatus.ok) and (
    results.solver.termination_condition == TerminationCondition.optimal):
    print("The model was solved to optimality.")
elif results.solver.termination_condition == TerminationCondition.infeasible:
    print("The model is infeasible.")
else:
    print(f"Solver Status: {results.solver.status}")
    print(f"Termination Condition: {results.solver.termination_condition}")
# Print the objective function value if solved optimally
if results.solver.status == SolverStatus.ok and results.solver.termination_condition == TerminationCondition.optimal:
    print(f"Objective function value_3: {value(model.obj3)}")
model.display()
opt_value_obj3 = model.obj3()
print(opt_value_obj3)

# Prepare data for export to Excel
parameters = {
    'Node': i,
    'Capacity': [capacity[node] for node in i],
    'Initial_Inventory': [Inventory[node] for node in i],
    'TTR': [TTR[node] for node in i],
    'GHG': [GHG[node] for node in i],
    'SI': [SI[node] for node in i]
}
bom_data = {
    'From_To': [f"{key[0]}_{key[1]}" for key in r.keys()],
    'Quantity': [value for value in r.values()]
}
demand_data = {
    'Product': list(demand.keys()),
    'Demand': list(demand.values())
}
ghg_flow_data = {
    'From_To': [f"{key[0]}_{key[1]}" for key in GHG1.keys()],
    'GHG1': list(GHG1.values())
}
results_data = {
    'Node': i,
    'u': [value(model.u[node]) for node in i],
}

flow_data = {
    'From_To': [f"{pair[0]}_{pair[1]}" for pair in j],
    'y': [value(model.y[pair]) for pair in j]
}

final_products_data = {
    'Product': k,
    'l': [value(model.l[product]) for product in k],
}

# Convert dictionaries to pandas DataFrames
parameters_df = pd.DataFrame(parameters)
results_df = pd.DataFrame(results_data)
flow_df = pd.DataFrame(flow_data)
final_products_df = pd.DataFrame(final_products_data)

# Combine BOM, Demand, and GHG1 into parameters
bom_df = pd.DataFrame(bom_data)
demand_df = pd.DataFrame(demand_data)
ghg_flow_df = pd.DataFrame(ghg_flow_data)

# Combine additional parameters into the parameters DataFrame
parameters_df = pd.concat([parameters_df, bom_df, demand_df, ghg_flow_df], axis=1)

# Write to Excel
with pd.ExcelWriter('supply_chain_results.xlsx') as writer:
    parameters_df.to_excel(writer, sheet_name='Parameters', index=False)
    results_df.to_excel(writer, sheet_name='Results', index=False)
    flow_df.to_excel(writer, sheet_name='Flow', index=False)
    final_products_df.to_excel(writer, sheet_name='FinalProducts', index=False)