import streamlit as st
import time
from miscellanious_functions import CreateInstance, SolutionPlot, PComparisonPlot
from p_algorithm import p_algorithm, lp_optimal


st.set_page_config(page_title = "Facility Location Problem Simulator", 
page_icon="🏬",
layout="wide"
)

st.title("Two-Echelon Facility Location Problem Simulator 🏭")
st.subheader("Manual Simulations")

with st.sidebar:
    st.subheader("Problem Instances")

    NoOfCustomers = st.number_input('Insert number of clients 🏬',
    min_value=1, 
    max_value=1000, 
    value=50,   
    step=1, 
    help="Insert the total number of clients that need to be served"
    )

    NoOfRegionalDepots = st.number_input('Insert number of regional depots 🏭',
    min_value=1, 
    max_value=20, 
    value=5,   
    step=1, 
    help="Insert the total number of clients that need to be served"
    )

    Seed = st.number_input('Insert seed number 🌱',
    min_value=1, 
    max_value=1000,  
    value=7, 
    step=1, 
    help="Seed is a number which makes python generate the same data in each execution"
    )

    GridSize = st.number_input('Insert grid size 📏',
    min_value=20, 
    max_value=500, 
    value=100, 
    step=5, 
    help="Grid is the size of the plot's height and width. It is also the maximum value a node's x and y coordinates can be equal to"
    )

    CostKm = st.number_input('Insert gas cost per km 🛢️',
    min_value=0.1, 
    max_value=1.5, 
    value=0.5, 
    step=0.1, 
    help="Grid is the size of the plot's height and width. It is also the maximum value a node's x and y coordinates can be equal to"
    )

    CostWarehouse = st.number_input('Insert operational cost per warehouse 🏭',
    min_value=0, 
    max_value=2000, 
    value=100, 
    step=100, 
    help="Grid is the size of the plot's height and width. It is also the maximum value a node's x and y coordinates can be equal to"
    )

    WarehouseLimit = st.number_input('Insert warehouse capacity limit 🏭',
    min_value=100,
    max_value=1000,
    value=500,
    step=100,
    help="Grid is the size of the plot's height and width. It is also the maximum value a node's x and y coordinates can be equal to"
    )

    #Create Disible Demand yes/no
    Divisible = st.radio("Is the demand divisible?", ("Yes", "No"))

    if Divisible == "Yes":
        Divisible = True
    else:
        Divisible = False
 
    st.subheader("Solution Method")

    option = st.selectbox(
    'Choose a Construction Algorithm:',
    ('LP Linear Programming'))


# Initializing the problem instances
inst = CreateInstance(NoOfCustomers, NoOfRegionalDepots, GridSize, Divisible, CostKm, CostWarehouse, WarehouseLimit, Seed)

stime = time.time()
cpu_stime = time.process_time()



col1, col2 = st.columns(2)

with col1:   
    st.header("Assignment Plot")
    solution = lp_optimal(inst)
    figure = SolutionPlot(inst, solution)   
    st.pyplot(fig=figure, use_container_width=True)
    #figure.savefig('plot.jpeg')

with col2:
    st.header("Cost Trade-off")
    p_vector = [0, 1, 2, 3, 4, NoOfRegionalDepots]
    solution_vector = []
    x_vector = []
    for p in p_vector:
        inst = CreateInstance(NoOfCustomers, NoOfRegionalDepots, GridSize, Divisible, CostKm, CostWarehouse, WarehouseLimit, Seed)
        solution = p_algorithm(inst, p)
        if solution['total_cost'] == 0:
            pass
        else:
            solution_vector.append(solution)
            x_vector.append(p)
    
    fig2 = PComparisonPlot(inst, x_vector, solution_vector)
    st.pyplot(fig=fig2, use_container_width=True)
    #fig2.savefig('plot2.jpeg')

    
