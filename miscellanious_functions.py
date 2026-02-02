import matplotlib.pyplot as plt
import random
import statistics
import pandas as pd
from openpyxl import Workbook
import time

def CreateInstance(NoOfCustomers, NoOfRegionalDepots, Grid, Divisible, CostKm, CostWarehouse, WarehouseLimit, Seed):
    
    random.seed(Seed)

    all_Depots = []
    all_Customers = [] # Lists with customers
    all_Nodes = []     # List with all Nodes (customers + depots)
    
    for i in range(1, int(NoOfCustomers)+1):
        cust = []
        cust = [i, random.randint(1, Grid), random.randint(1, Grid), random.randint(1, 1)]
        all_Customers.append(cust)
        all_Nodes.append(cust)
    
    random.seed(Seed)
    
    for i in range(1, int(NoOfRegionalDepots)+2):
        if i == 1:
            dep = [1000+i, int(Grid/2), int(Grid/2), True]      
        else:
            dep = [1000+i, random.randint(1, Grid), random.randint(1, Grid), False]      
   
        all_Depots.append(dep)
    
    for depot in all_Depots: # Appending the depots to the list of lists that includes all nodes
        all_Nodes.append(depot)
        
    return {"allCustomers": all_Customers, 
            "allNodes": all_Nodes, 
            "allDepots": all_Depots,
            "GridSize": Grid,
            "Divisible": Divisible,
            "CostKm": CostKm,
            "CostWarehouse": CostWarehouse,
            "WarehouseLimit": WarehouseLimit,
            "Seed": Seed}
    # all_Customers and All_Nodes are lists of lists. Format is [id, x, y].   


def SolutionPlot(inst, solution):

    all_Customers = inst["allCustomers"]
    all_Depots = inst["allDepots"]
    GridSize = inst["GridSize"]
    Divisible = inst["Divisible"]

    assigned_customers = solution["assigned_customers"]
    used_warehouses = solution["used_warehouses"]

    '''
    This function creates a "matplotlib" figure with the MDVRP solution.
    '''
    fig, ax = plt.subplots(figsize=(8, 6))  # same for both functions

    all_colors = ['yellow', 'red', 'green', 'blue', 'purple', 'orange', 'pink', 'brown', 'gray', 'olive', 'cyan', 'magenta', 'lime', 'teal', 'indigo', 'maroon', 'navy', 'peru', 'rosybrown', 'sienna', 'tan', 'darkorange', 'gold', 'darkkhaki', 'olivedrab', 'yellowgreen', 'darkseagreen', 'lightseagreen', 'darkcyan', 'deepskyblue', 'dodgerblue', 'royalblue', 'blueviolet', 'darkorchid', 'mediumvioletred', 'crimson', 'firebrick', 'darkred', 'darkslategray', 'dimgray', 'black']
    
    #Plot the customers with circles (the size of the circle is proportional to the demand and the color is proportional to the depot)
    if Divisible:
        for customer in all_Customers:
            assigned_depots = assigned_customers[customer[0]]
            if len(assigned_depots) == 1:
                ax.plot(customer[1], customer[2], 'o', markersize=customer[3]*10, color=all_colors[assigned_depots[0]-1000])
            else:
                # Plot the circle with the color of all depots (half for each depot)
                ax.plot(customer[1], customer[2], 'o', markersize=customer[3]*10, color=all_colors[assigned_depots[0]-1000], alpha=0.5)
                ax.plot(customer[1], customer[2], 'o', markersize=customer[3]*10, color=all_colors[assigned_depots[1]-1000], alpha=0.5)
    else:
        for customer in all_Customers:
            ax.plot(customer[1], customer[2], 'o', markersize=customer[3]*10, color=all_colors[assigned_customers[customer[0]]-1000])

    #Plot the depots with squares
    for depot in all_Depots:
        if depot[3] == True:
            if depot[0] in used_warehouses:
                ax.plot(depot[1], depot[2], 'D', markersize=20, color=all_colors[depot[0]-1000])  # Diamond shape
            else:
                ax.plot(depot[1], depot[2], 'D', markersize=20, color='black')  # Diamond shape
        else:
            if depot[0] in used_warehouses:
                ax.plot(depot[1], depot[2], 'ks', markersize=15, color=all_colors[depot[0]-1000])
            else:
                ax.plot(depot[1], depot[2], 'ks', markersize=15, color='black')

    # Show the plot.
    fig.set_size_inches(8, 8)

    plt.xlim([0, GridSize])
    plt.ylim([0, GridSize])
    plt.style.use("default") # seaborn, default, seaborn-pastel

    # Create a legend for the depot and customer shapes
    legend_elements = [
        plt.Line2D([0], [0], marker='D', color='w', label='Central depot', markerfacecolor='black', markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label='Regional depot', markerfacecolor='black', markersize=10),
        plt.Line2D([0], [0], marker='o', color='w', label='Customer', markerfacecolor='black', markersize=10)
    ]
    ax.legend(handles=legend_elements, loc='lower center')



    return fig

def PComparisonPlot(inst, p_vector, solution_vector):

    number_of_scenarios = len(p_vector)

    scenarios = []

    for p, sol in zip(p_vector, solution_vector):
        
        inbound_cost = sol["inbound_cost"]
        outbound_cost = sol["outbound_cost"]
        warehouse_cost = sol["warehouse_cost"]
        total_cost = inbound_cost + outbound_cost + warehouse_cost

        scenarios.append({"p": p, "inbound_cost": inbound_cost, "outbound_cost": outbound_cost, "total_cost": total_cost, "warehouse_cost": warehouse_cost})

    #Plot the results

    df = pd.DataFrame(scenarios)

    fig, ax = plt.subplots(figsize=(8, 6))  # same for both functions

    ax.plot(df["p"], df["inbound_cost"], label="Inbound cost")
    ax.plot(df["p"], df["outbound_cost"], label="Outbound cost")
    ax.plot(df["p"], df["total_cost"], label="Total cost")
    ax.plot(df["p"], df["warehouse_cost"], label="Warehouse cost")

    ax.set_xlabel("Number of regional depots")
    ax.set_ylabel("Cost")
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

    return fig