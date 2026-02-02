#p algorithm for facility location

import gurobipy as gp
from gurobipy import GRB

def lp_optimal(inst):
    
    # Extracting the data from the instance

    all_Customers = inst["allCustomers"]
    all_Depots = inst["allDepots"]
    all_Nodes = inst["allNodes"]
    Seed = inst["Seed"]
    Divisible = inst["Divisible"]
    CostKm = inst["CostKm"]
    CostWarehouse = inst["CostWarehouse"]
    WarehouseLimit = inst["WarehouseLimit"]

    # Create sets

    N_customers = [i[0] for i in all_Customers] # Set of customers
    N_depots = [i[0] for i in all_Depots] # Set of depots
    N = N_customers + N_depots # Set of all nodes


    # Create a dictionary to store the Euclidean distance between nodes

    dist = {(i[0], j[0]): round(((i[1]-j[1])**2 + (i[2]-j[2])**2)**0.5, 2) for i in all_Nodes for j in all_Nodes if i[0] != j[0]}
    cost = {(i[0], j[0]): round(CostKm*dist[i[0], j[0]], 2) for i in all_Nodes for j in all_Nodes if i != j}
    time = {(i[0], j[0]): round(dist[i[0], j[0]]/30, 2) for i in all_Nodes for j in all_Nodes if i != j}

    # Create a dictionary to store the demand of each customer
    demand = {i[0]: i[3] for i in all_Customers}

    # Create a dictionary to store the capacity of each depot
    capacity = {i[0]: WarehouseLimit if i[3] == True else 10000 for i in all_Depots}

    #Create a binary variable to indicate if the depot is central
    central = {i[0]: 1 if i[3] == True else 0 for i in all_Depots}

    # Decision variables

    m = gp.Model("p_algorithm")
    if Divisible:
        x = m.addVars(N_customers, N_depots, vtype=GRB.CONTINUOUS, name="x")
    else:
        x = m.addVars(N_customers, N_depots, vtype=GRB.BINARY, name="x")
    y = m.addVars(N_depots, vtype=GRB.BINARY, name="y")
    inbound_cost = m.addVar(vtype=GRB.CONTINUOUS, name="inbound_cost")
    outbound_cost = m.addVar(vtype=GRB.CONTINUOUS, name="outbound_cost")
    warehouse_cost = m.addVar(vtype=GRB.CONTINUOUS, name="warehouse_cost")

    # Objective function

    m.setObjective(inbound_cost + outbound_cost + warehouse_cost, GRB.MINIMIZE)

    # Constraints

    m.addConstrs(gp.quicksum(x[i, j] for j in N_depots) == 1 for i in N_customers)

    m.addConstrs(gp.quicksum(x[i, j]*demand[i] for i in N_customers) <= capacity[j] * y[j] for j in N_depots)

    m.addConstr(inbound_cost == gp.quicksum(cost[i, j] * x[i, j] for i in N_customers for j in N_depots if central[j] == 0))

    m.addConstr(outbound_cost == gp.quicksum(cost[i, j] * x[i, j] for i in N_customers for j in N_depots if central[j] == 1))

    m.addConstr(warehouse_cost == gp.quicksum(CostWarehouse * y[j] for j in N_depots))

    #m.addConstr(gp.quicksum(y[j] for j in N_depots if central[j] == 0) == 0)

    # Optimize the model

    m.optimize()

    if m.status == GRB.INFEASIBLE:
        solution = {"assigned_customers": {},
                "used_warehouses": [],
                "inbound_cost": 0,
                "outbound_cost": 0,
                "warehouse_cost": 0,
                "total_cost": 0}
    else:

        if Divisible:
            solution = {"assigned_customers": {i: [j for j in N_depots if x[i, j].x > 0] for i in N_customers},
                        "used_warehouses": [j for j in N_depots if y[j].x == 1] + [1001],
                        "inbound_cost": inbound_cost.x,
                        "outbound_cost": outbound_cost.x,
                        "warehouse_cost": warehouse_cost.x,
                        "total_cost": m.objVal}
        else:

            # Create a dictionary to store the solution
            solution = {"assigned_customers": {i: j for i in N_customers for j in N_depots if x[i, j].x == 1},
                        "used_warehouses": [j for j in N_depots if y[j].x == 1] + [1001],
                        "inbound_cost": inbound_cost.x,
                        "outbound_cost": outbound_cost.x,
                        "warehouse_cost": warehouse_cost.x,
                        "total_cost": m.objVal}

    return solution

def p_algorithm(inst, p_regional):

    # Extracting the data from the instance

    all_Customers = inst["allCustomers"]
    all_Depots = inst["allDepots"]
    all_Nodes = inst["allNodes"]
    GridSize = inst["GridSize"]
    Seed = inst["Seed"]
    Divisible = inst["Divisible"]
    CostKm = inst["CostKm"]
    CostWarehouse = inst["CostWarehouse"]
    WarehouseLimit = inst["WarehouseLimit"]

    # Create sets

    N_customers = [i[0] for i in all_Customers] # Set of customers
    N_depots = [i[0] for i in all_Depots] # Set of depots
    N = N_customers + N_depots # Set of all nodes


    # Create a dictionary to store the Euclidean distance between nodes


    dist = {(i[0], j[0]): round(((i[1]-j[1])**2 + (i[2]-j[2])**2)**0.5, 2) for i in all_Nodes for j in all_Nodes if i[0] != j[0]}
    cost = {(i[0], j[0]): round(CostKm*dist[i[0], j[0]], 2) for i in all_Nodes for j in all_Nodes if i != j}
    time = {(i[0], j[0]): round(dist[i[0], j[0]]/30, 2) for i in all_Nodes for j in all_Nodes if i != j}

    # Create a dictionary to store the demand of each customer
    demand = {i[0]: i[3] for i in all_Customers}

    # Create a dictionary to store the capacity of each depot
    capacity = {i[0]: WarehouseLimit if i[3] == True else 10000 for i in all_Depots}

    #Create a binary variable to indicate if the depot is central
    central = {i[0]: 1 if i[3] == True else 0 for i in all_Depots}

    # Decision variables

    m = gp.Model("p_algorithm")

    if Divisible:
        x = m.addVars(N_customers, N_depots, vtype=GRB.CONTINUOUS, name="x")
    else:
        x = m.addVars(N_customers, N_depots, vtype=GRB.BINARY, name="x")
    y = m.addVars(N_depots, vtype=GRB.BINARY, name="y")
    inbound_cost = m.addVar(vtype=GRB.CONTINUOUS, name="inbound_cost")
    outbound_cost = m.addVar(vtype=GRB.CONTINUOUS, name="outbound_cost")
    warehouse_cost = m.addVar(vtype=GRB.CONTINUOUS, name="warehouse_cost")

    # Objective function

    m.setObjective(inbound_cost + outbound_cost, GRB.MINIMIZE)

    # Constraints

    m.addConstrs(gp.quicksum(x[i, j] for j in N_depots) == 1 for i in N_customers)

    m.addConstrs(gp.quicksum(x[i, j] * demand[i] for i in N_customers) <= capacity[j] * y[j] for j in N_depots)

    m.addConstr(gp.quicksum(y[j] for j in N_depots if central[j] == 0) == p_regional)

    m.addConstr(inbound_cost == gp.quicksum(cost[i, j] * x[i, j] for i in N_customers for j in N_depots if central[j] == 0))

    m.addConstr(outbound_cost == gp.quicksum(cost[i, j] * x[i, j] for i in N_customers for j in N_depots if central[j] == 1))

    m.addConstr(warehouse_cost == gp.quicksum(CostWarehouse * y[j] for j in N_depots))

    # Optimize the model

    m.optimize()

    if m.status == GRB.INFEASIBLE:
        solution = {"assigned_customers": {},
                "used_warehouses": [],
                "inbound_cost": 0,
                "outbound_cost": 0,
                "warehouse_cost": 0,
                "total_cost": 0}
    else:
        
        if Divisible:

            # Create a dictionary to store the solution
            solution = {"assigned_customers": {i: [j for j in N_depots if x[i, j].x > 0] for i in N_customers},
                        "used_warehouses": [j for j in N_depots if y[j].x == 1] + [1001],
                        "inbound_cost": inbound_cost.x,
                        "outbound_cost": outbound_cost.x,
                        "warehouse_cost": warehouse_cost.x,
                        "total_cost": m.objVal}
        else:   

            # Create a dictionary to store the solution
            solution = {"assigned_customers": {i: j for i in N_customers for j in N_depots if x[i, j].x == 1},
                        "used_warehouses": [j for j in N_depots if y[j].x == 1] + [1001],
                        "inbound_cost": inbound_cost.x,
                        "outbound_cost": outbound_cost.x,
                        "warehouse_cost": warehouse_cost.x,
                        "total_cost": m.objVal}

    return solution

'''
# Test the function

from miscellanious_functions import CreateInstance, SolutionPlot, PComparisonPlot

inst = CreateInstance(100, 7, 100, False, 1, 5, 1)
solution = p_algorithm(inst)

fig1 = SolutionPlot(inst, solution)

import matplotlib.pyplot as plt

# Show the plot
plt.show()

solution_vector = []
list_p_regional = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for p in list_p_regional:
    inst = CreateInstance(100, 11, 100, False, 1, p, 1)
    solution = p_algorithm(inst)
    solution_vector.append(solution)

fig2 = PComparisonPlot(inst, list_p_regional, solution_vector)

plt.show()
'''
    











    




