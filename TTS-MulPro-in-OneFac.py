from pyomo.environ import *
import random
import pandas as pd

random.seed(5)

# Create a Concrete Model
m = ConcreteModel()

# Sets
# set of all factories
m.Factories = Set(initialize=['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11'])
# set of All products
m.Products = Set(initialize=['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P12', 'P13', 'P14', 'P15', 'P16', 'P17',
     'P18', 'P19', 'P20'])

m.Factory_Product =Set(dimen=2, initialize=[('F1','P1'), ('F1', 'P2'), ('F2','P3'), ('F2','P4'), ('F2','P5'),('F3','P6'), ('F3','P7'), ('F3','P8'),('F4','P9'), ('F4','P10'),
     ('F5','P11'),  ('F6','P12'), ('F6','P13'),('F7','P14'), ('F7','P15'), ('F8','P16'), ('F8','P17'), ('F9','P18'),('F10','P19'),('F11','P20')])

# set of flows
m.Flows = Set(dimen=4, initialize=[('F1','P1','F4', 'P9'), ('F1','P1', 'F10', 'P19'), ('F1', 'P2','F4','P9'), ('F1','P2','F7','P15'), ('F1','P2','F11','P20'), ('F2','P3','F4','P10'),
     ('F2','P3','F8','P16'),('F2','P4','F5','P11'), ('F2','P5','F5','P11'),('F3','P6','F5','P11'), ('F3','P6','F8','P17'), ('F3','P7','F6','P12'), ('F3','P7','F6','P13'),
     ('F3','P7','F7','P14'), ('F3','P7','F9','P18'), ('F3','P8','F6','P13'),('F4','P9','F7','P14'), ('F4','P9','F10','P19'),('F4','P10','F7','P14'), ('F4','P10','F7','P15'),
     ('F4','P10','F11','P20'), ('F5','P11','F7','P14'), ('F5','P11','F8','P16'), ('F6','P12','F7','P15'), ('F6','P12','F8','P16'),('F6','P12','F8','P17'),('F6','P13','F8','P17'),
     ('F6','P13','F9','P18'), ('F7','P14','F9','P18'), ('F7','P15','F9','P18'), ('F7','P15','F10','P19'), ('F8','P16','F10','P19'), ('F8','P16','F11','P20'),('F8','P17','F11','P20')])

# set of distance between factories
m.Factory_Relation = Set(dimen=2, initialize=[('F1','F4'), ('F1','F10'), ('F1','F7'), ('F1','F11'), ('F2','F4'),('F2','F8'),('F2','F5'),('F3','F5'), ('F3','F8'), ('F3','F6'),('F3','F7'), ('F3','F9'),
       ('F4','F7'), ('F4','F10'),('F4','F11'), ('F5','F7'), ('F5','F8'), ('F6','F7'), ('F6','F8'),('F6','F9'), ('F7','F9'), ('F7','F10'), ('F8','F10'), ('F8','F11')])

# set of final products
m.Final_Products = Set(initialize=['P18', 'P19', 'P20'])

# set of final factories
m.Final_Factories = Set(initialize=['F9', 'F10', 'F11'])

m.Requirements =Set(dimen=2, initialize= [('P1', 'P9'), ('P1', 'P19'), ('P2', 'P9'), ('P2', 'P15'), ('P2', 'P20'), ('P3', 'P10'), ('P3', 'P16'),
     ('P4', 'P11'), ('P5', 'P11'),('P6', 'P11'), ('P6', 'P17'), ('P7', 'P12'), ('P7', 'P13'), ('P7', 'P14'), ('P7', 'P18'), ('P8', 'P13'),
     ('P9', 'P14'), ('P9', 'P19'),('P10', 'P14'), ('P10', 'P15'), ('P10', 'P20'), ('P11', 'P14'), ('P11', 'P16'), ('P12', 'P15'), ('P12', 'P16'),
     ('P12', 'P17'),('P13', 'P17'), ('P13', 'P18'), ('P14', 'P18'), ('P15', 'P18'), ('P15', 'P19'), ('P16', 'P19'), ('P16', 'P20'),('P17', 'P20')])
# Parameters
# BOM relationship
m.BOM = Param(m.Requirements, initialize={('P1', 'P9'): 4, ('P1', 'P19'): 11, ('P2', 'P9'): 2, ('P2', 'P15'): 8, ('P2', 'P20'): 16, ('P3', 'P10'): 4,
     ('P3', 'P16'): 6, ('P4', 'P11'): 2,('P5', 'P11'): 3, ('P6', 'P11'): 2, ('P6', 'P17'): 12, ('P7', 'P12'): 1, ('P7', 'P13'): 1, ('P7', 'P14'): 5,
     ('P7', 'P18'): 15,('P8', 'P13'): 4,('P9', 'P14'): 1, ('P9', 'P19'): 3, ('P10', 'P14'): 1, ('P10', 'P15'): 2, ('P10', 'P20'): 4, ('P11', 'P14'): 1,
     ('P11', 'P16'): 1,('P12', 'P15'): 2, ('P12', 'P16'): 1, ('P12', 'P17'): 3, ('P13', 'P17'): 4, ('P13', 'P18'): 10, ('P14', 'P18'): 2,
     ('P15', 'P18'): 1,('P15', 'P19'): 1, ('P16', 'P19'): 2, ('P16', 'P20'): 1, ('P17', 'P20'): 2})

m.Demand = Param(m.Products, initialize={'P18': 500, 'P19': 400, 'P20': 600})
# parameters-capacity
m.Capacity = Param(m.Factories, initialize={i: random.randint(5000, 15000) for i in m.Factories})

# parameters-Initial Inventory
m.Inventory = Param(m.Factory_Product, initialize= {i: random.randint(100, 200) for i in m.Factory_Product})

# Variables
m.u = Var(m.Factory_Product, within=NonNegativeReals)
m.y = Var(m.Flows, within=NonNegativeReals)
m.TTS = Var(within=NonNegativeReals)

# Objective functions
Obj = m.TTS
m.obj = Objective(expr=Obj, sense=maximize)

# constraints
m.Constraints = ConstraintList()

# BOM constraints
for (i, j) in m.Requirements:
    for h in m.Factories:
        for f in m.Factories:
            if (f, i, h, j) in m.Flows:
                m.Constraints.add(m.u[h, j] * m.BOM[i, j] <= sum(m.y[f, i, h, j] for f in m.Factories if (f, i, h, j) in m.Flows))

# production and inventory
for f in m.Factories:
    for i in m.Products:
        if (f, i) in m.Factory_Product:
            m.Constraints.add(sum(m.y[f, i, h, j] for h in m.Factories for j in m.Products if (f, i, h, j) in m.Flows) <= m.u[f, i] + m.Inventory[f, i])

# Demand satisfying
for i in m.Final_Products:
    m.Constraints.add(sum(m.u[f,i] + m.Inventory[f,i] for f in m.Final_Factories if (f,i) in m.Factory_Product) >= m.Demand[i] * m.TTS)

# Capacity constraint
for f in m.Factories:
    m.Constraints.add(sum(1 * m.u[f,i] for i in m.Products if (f,i) in m.Factory_Product) <= m.Capacity[f] * m.TTS)

# solver
solver = SolverFactory('cbc')
# m.display()
# m.pprint()

# Disruption scenarios
m.Constraints.add(m.u['F2','P5'] <= 0)

results = solver.solve(m, tee=True)
# Check the status of the model
if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
    print("The model was solved to optimality.")
elif results.solver.termination_condition == TerminationCondition.infeasible:
    print("The model is infeasible.")
else:
    print(f"Solver Status: {results.solver.status}")
    print(f"Termination Condition: {results.solver.termination_condition}")
#  Print the objective function value if solved optimally
if results.solver.status == SolverStatus.ok and results.solver.termination_condition == TerminationCondition.optimal:
    print(f"Objective function value_1: {value(m.obj)}")
m.display()
opt_value_obj = m.obj()



