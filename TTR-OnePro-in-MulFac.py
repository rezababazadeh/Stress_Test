from pyomo.environ import *
import random
import pandas as pd

random.seed(5)

# Create a Concrete Model
m = ConcreteModel()

# Sets
# set of all factories
m.Factories = Set(initialize=['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11','F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19', 'F20',
                              'F21', 'F22','F23', 'F24', 'F25', 'F26', 'F27', 'F28', 'F29', 'F30', 'F31', 'F32', 'F33', 'F34', 'F35'])
# set of All products
m.Products = Set(initialize=['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P12', 'P13', 'P14','P15', 'P16', 'P17', 'P18', 'P19', 'P20'])

m.Factory_Product =Set(dimen=2, initialize=[('F1','P1'), ('F2','P1'), ('F3', 'P2'), ('F4','P3'),('F5','P3'),('F6','P3'), ('F7','P4'), ('F8','P5'),('F9','P5'),('F10','P6'),('F11','P6'),
('F12','P7'), ('F13','P8'),('F14','P8'),('F15','P9'),('F16','P9'), ('F17','P10'),('F18','P11'),('F19','P11'),('F20','P12'),('F21','P13'),('F22','P13'),('F23','P14'),('F24','P14'),
 ('F25','P15'), ('F26','P16'), ('F27','P17'),('F28','P17'),('F29','P18'),('F30','P18'),('F31','P19'),('F32','P19'),('F33','P20'),('F34','P20'),('F35','P20')])

# set of distance between factories
m.Factory_Relation = Set(dimen=2, initialize=[
    ('F1', 'F15'), ('F1', 'F16'), ('F2', 'F15'), ('F2', 'F16'),
    ('F1', 'F31'), ('F1', 'F32'), ('F2', 'F31'), ('F2', 'F32'),
    ('F3', 'F15'), ('F3', 'F16'), ('F3', 'F25'),
    ('F3', 'F33'), ('F3', 'F34'), ('F3', 'F35'),
    ('F4', 'F17'), ('F5', 'F17'), ('F6', 'F17'),
    ('F4', 'F26'), ('F5', 'F26'), ('F6', 'F26'),
    ('F7', 'F18'), ('F7', 'F19'),
    ('F8', 'F18'), ('F8', 'F19'), ('F9', 'F18'), ('F9', 'F19'),
    ('F10', 'F18'), ('F11', 'F18'), ('F10', 'F19'), ('F11', 'F19'),
    ('F10', 'F27'), ('F11', 'F27'), ('F10', 'F28'), ('F11', 'F28'),
    ('F12', 'F20'), ('F12', 'F21'), ('F12', 'F22'),
    ('F12', 'F23'), ('F12', 'F24'), ('F12', 'F29'), ('F12', 'F30'),
    ('F13', 'F21'), ('F14', 'F21'), ('F13', 'F22'), ('F14', 'F22'),
    ('F15', 'F23'), ('F16', 'F23'), ('F15', 'F24'), ('F16', 'F24'),
    ('F15', 'F31'), ('F16', 'F31'), ('F15', 'F32'), ('F16', 'F32'),
    ('F17', 'F23'), ('F17', 'F24'), ('F17', 'F25'),
    ('F17', 'F33'), ('F17', 'F34'), ('F17', 'F35'),
    ('F18', 'F23'), ('F19', 'F23'), ('F18', 'F24'), ('F19', 'F24'),
    ('F18', 'F26'), ('F19', 'F26'),
    ('F20', 'F25'), ('F20', 'F26'), ('F20', 'F27'), ('F20', 'F28'),
    ('F21', 'F27'), ('F22', 'F27'), ('F21', 'F28'), ('F22', 'F28'),
    ('F21', 'F29'), ('F22', 'F29'), ('F21', 'F30'), ('F22', 'F30'),
    ('F23', 'F29'), ('F24', 'F29'), ('F23', 'F30'), ('F24', 'F30'),
    ('F25', 'F29'), ('F25', 'F30'), ('F25', 'F31'), ('F25', 'F32'),
    ('F26', 'F31'), ('F26', 'F32'), ('F26', 'F33'), ('F26', 'F34'), ('F26', 'F35'),
    ('F27', 'F33'), ('F27', 'F34'), ('F27', 'F35'), ('F28', 'F33'), ('F28', 'F34'), ('F28', 'F35')])

# set of final products
m.Final_Products = Set(initialize=['P18', 'P19', 'P20'])

# set of final factories
m.Final_Factories = Set(initialize=['F29', 'F30', 'F31', 'F32', 'F33', 'F34', 'F35'])

# set of Flows
m.Flows = Set(dimen=4, initialize=[
('F1','P1','F15', 'P9'),('F1','P1','F16', 'P9'),('F2','P1','F15', 'P9'),('F2','P1','F16', 'P9'),
('F1','P1','F31', 'P19'),('F1','P1','F32', 'P19'),('F2','P1','F31', 'P19'),('F2','P1','F32', 'P19'),
('F3','P2','F15', 'P9'),('F3','P2','F16', 'P9'),
('F3','P2','F25', 'P15'),
('F3','P2','F33', 'P20'),('F3','P2','F34', 'P20'),('F3','P2','F35', 'P20'),
('F4','P3','F17', 'P10'),('F5','P3','F17', 'P10'),('F6','P3','F17', 'P10'),('F4','P3','F26', 'P16'),('F5','P3','F26', 'P16'),('F6','P3','F26', 'P16'),
('F7','P4','F18', 'P11'),('F7','P4','F19', 'P11'),
('F8','P5','F18', 'P11'),('F8','P5','F19', 'P11'),('F9','P5','F18', 'P11'),('F9','P5','F19', 'P11'),
('F10','P6','F18', 'P11'),('F11','P6','F18', 'P11'),('F10','P6','F19', 'P11'),('F11','P6','F19', 'P11'),
('F10','P6','F27', 'P17'),('F11','P6','F27', 'P17'),('F10','P6','F28', 'P17'),('F11','P6','F28', 'P17'),
('F12','P7','F20', 'P12'),
('F12','P7','F21', 'P13'),('F12','P7','F22', 'P13'),
('F12','P7','F23', 'P14'),('F12','P7','F24', 'P14'),
('F12','P7','F29', 'P18'),('F12','P7','F30', 'P18'),
('F13','P8','F21', 'P13'),('F14','P8','F21', 'P13'),('F13','P8','F22', 'P13'),('F14','P8','F22', 'P13'),
('F15','P9','F23', 'P14'),('F16','P9','F23', 'P14'),('F15','P9','F24', 'P14'),('F16','P9','F24', 'P14'),
('F15','P9','F31', 'P19'),('F16','P9','F31', 'P19'),('F15','P9','F32', 'P19'),('F16','P9','F32', 'P19'),
('F17','P10','F23', 'P14'),('F17','P10','F24', 'P14'),
('F17','P10','F25', 'P15'),
('F17','P10','F33', 'P20'),('F17','P10','F34', 'P20'),('F17','P10','F35', 'P20'),
('F18','P11','F23', 'P14'),('F19','P11','F23', 'P14'),('F18','P11','F24', 'P14'),('F19','P11','F24', 'P14'),
('F18','P11','F26', 'P16'),('F19','P11','F26', 'P16'),
('F20','P12','F25', 'P15'),
('F20','P12','F26', 'P16'),
('F20','P12','F27', 'P17'),('F20','P12','F28', 'P17'),
('F21','P13','F27', 'P17'),('F22','P13','F27', 'P17'),('F21','P13','F28', 'P17'),('F22','P13','F28', 'P17'),
('F21','P13','F29', 'P18'),('F22','P13','F29', 'P18'),('F21','P13','F30', 'P18'),('F22','P13','F30', 'P18'),
('F23','P14','F29', 'P18'),('F24','P14','F29', 'P18'),('F23','P14','F30', 'P18'),('F24','P14','F30', 'P18'),
('F25','P15','F29', 'P18'),('F25','P15','F30', 'P18'),
('F25','P15','F31', 'P19'),('F25','P15','F32', 'P19'),
('F26','P16','F31', 'P19'),('F26','P16','F32', 'P19'),
('F26','P16','F33', 'P20'),('F26','P16','F34', 'P20'),('F26','P16','F35', 'P20'),
('F27','P17','F33', 'P20'),('F27','P17','F34', 'P20'),('F27','P17','F35', 'P20'),('F28','P17','F33', 'P20'),('F28','P17','F34', 'P20'),('F28','P17','F35', 'P20')])

m.Requirements = Set(dimen=2, initialize= [('P1', 'P9'), ('P1', 'P19'), ('P2', 'P9'), ('P2', 'P15'), ('P2', 'P20'), ('P3', 'P10'), ('P3', 'P16'),
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

# parameters-Time to recover (Optimistic: the larsgest TTR in disruption Sc, Pessimistic: the Lowest TTR in the sc,
# Most likely velue: Average on all TTRs in the scenarion)
TTR = 6

# parameters-profit margin
m.Profitmargin = Param(m.Final_Products,initialize={i: random.randint(400, 800) for i in m.Final_Products})

# parameters-GHG at each node
m.PGHG = Param(m.Factory_Product, initialize={i: random.randint(20, 35) for i in m.Factory_Product})

# parameters-TGHG in flow between nodes for transporting one unit per kilometer
TGHG=5
m.Distance = Param(m.Factory_Relation, initialize={i: random.randint(50, 300) for i in m.Factory_Relation})

# parameters-Societal impact of each node
m.SI = Param(m.Factories, initialize={i: random.randint(1, 10) for i in m.Factories})

# Variables
m.u = Var(m.Factory_Product, within=NonNegativeReals)
m.y = Var(m.Flows, within=NonNegativeReals)
m.l = Var(m.Final_Products, within=NonNegativeReals)

# Objective functions
Obj1 = sum(m.Profitmargin[i] * m.l[i] for i in m.Final_Products)
m.obj1 = Objective(expr=Obj1, sense=minimize)

Obj2 = sum(m.PGHG[i,j] * m.u[i,j] for i,j in m.Factory_Product) +sum(TGHG * m.Distance[f1, f2] * m.y[f1, p1, f2, p2] for (f1, p1, f2, p2) in m.Flows if (f1, f2) in m.Distance)
m.obj2 = Objective(expr=Obj2, sense=minimize)

Obj3 = sum(m.SI[f] * m.u[f, i] for (f,i) in m.Factory_Product)
m.obj3 = Objective(expr=Obj3, sense=maximize)

# constraints
m.Constraints = ConstraintList()

# BOM constraints
for (i, j) in m.Requirements:
    for h in m.Factories:
        for f in m.Factories:
            if (f, i, h, j) in m.Flows:
                m.Constraints.add(m.u[h, j] * m.BOM[i, j] <= sum(m.y[f, i, h, j] for f in m.Factories if (f, i, h, j) in m.Flows))

#Production and Inventory constraint
for f in m.Factories:
    for i in m.Products:
        if (f,i) in m.Factory_Product:
            m.Constraints.add(sum(m.y[f, i, h, j] for h in m.Factories for j in m.Products if (f, i, h, j) in m.Flows)<= m.u[f, i] + m.Inventory[f, i])

# Demand satisfying
for i in m.Final_Products:
    m.Constraints.add(m.l[i] + sum(m.u[f,i] + m.Inventory[f,i] for f in m.Final_Factories if (f,i) in m.Factory_Product) >= m.Demand[i] * TTR)

# solver# Upper bound for lost sales
for i in m.Final_Products:
    m.Constraints.add(m.l[i] <= m.Demand[i] * TTR)

# Capacity constraint
for f in m.Factories:
    m.Constraints.add(sum(1 * m.u[f,i] for i in m.Products if (f,i) in m.Factory_Product) <= m.Capacity[f] * TTR)

solver = SolverFactory('cbc')
# m.display()
m.pprint()
# Disruption scenarios
m.Constraints.add(m.u['F8','P5'] <= 0)

# Step 1: Optimize the first objective
m.obj2.deactivate()
m.obj3.deactivate()
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
    print(f"Objective function value_1: {value(m.obj1)}")
# m.display()
opt_value_obj1 = m.obj1()

# Step 2: Optimize the second objective
# Fixing optimal value for the first objective function
m.Constraints.add((sum(m.Profitmargin[i] * m.l[i] for i in m.Final_Products))  <= opt_value_obj1+0.3)
m.obj2.activate()
m.obj1.deactivate()
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
    print(f"Objective function value_2: {value(m.obj2)}")
# m.display()
opt_value_obj2 = m.obj2()

# Step 3: Optimize the third objective
# Fixing optimal value for the second objective function
m.Constraints.add((sum(m.PGHG[i,j] * m.u[i,j] for i,j in m.Factory_Product) +sum(TGHG * m.Distance[f1, f2] * m.y[f1, p1, f2, p2] for (f1, p1, f2, p2) in m.Flows if (f1, f2) in m.Distance))  <= opt_value_obj2+0.3)
m.obj3.activate()
m.obj2.deactivate()
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
    print(f"Objective function value_3: {value(m.obj3)}")
m.display()
opt_value_obj3 = m.obj3()
print(opt_value_obj3)

