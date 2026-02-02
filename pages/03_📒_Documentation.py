import streamlit as st
from PIL import Image
import numpy as np

# Title.
st.title("🔎Documentation🔍")

st.markdown("""
**Table of Contents**: <br>
<ul>
    <li>1. <a href="#1-introduction">Introduction</a></li>
    <li>2. <a href="#2-mathematical-model">Mathematical Model</a></li>
    <li>3. <a href="#3-cost-structure-analysis">Cost Structure Analysis</a></li>
</ul>
""", unsafe_allow_html=True)


st.markdown("## 1. Introduction")

st.write("""
This application studies a **Two-Echelon Facility Location Assignment Problem (2E-FLAP)**, where customer demand is
served through a network consisting of **regional depots** and **central warehouses**.
Each customer must be assigned to exactly one open facility, while facilities are subject to capacity constraints
and fixed opening costs.

The main objective is not only to find a cost-optimal assignment, but also to **visualize how changes in the cost
structure affect the total system cost**. In particular, the model explicitly decomposes the objective into:

• **Inbound transportation costs** (customer → regional depots)  
• **Outbound transportation costs** (customer → central warehouses)  
• **Warehouse opening costs**

This decomposition allows decision-makers to explore trade-offs between transportation intensity and infrastructure
investment, and to analyze how different cost regimes influence the optimal network design.
""")

st.markdown("## 2. Mathematical Model")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Sets")
    st.markdown("* **C**: set of customers")
    st.markdown("* **D**: set of candidate depots (regional and central)")
    
    st.markdown("### Indices")
    st.markdown("* *i* ∈ C: customer index")
    st.markdown("* *j* ∈ D: depot index")

with col2:
    st.markdown("### Parameters")
    st.markdown("* *dᵢ*: demand of customer *i*")
    st.markdown("* *capⱼ*: capacity of depot *j*")
    st.markdown("* *fⱼ*: fixed opening cost of depot *j*")
    st.markdown("* *cᵢⱼ*: transportation cost between customer *i* and depot *j*")
    st.markdown("* *zⱼ*: binary parameter indicating if depot *j* is central")

st.markdown("### Decision Variables")

st.markdown("""
* **xᵢⱼ** ∈ {0,1} or ℝ⁺ : fraction of customer *i*'s demand assigned to depot *j*  
* **yⱼ** ∈ {0,1} : 1 if depot *j* is opened, 0 otherwise  
""")

st.markdown("### Objective Function")

st.latex(r"""
\min \; 
\underbrace{\sum_{i \in C} \sum_{j \in D \,:\, z_j = 0} c_{ij} x_{ij}}_{\text{Inbound transportation cost}}
\;+\;
\underbrace{\sum_{i \in C} \sum_{j \in D \,:\, z_j = 1} c_{ij} x_{ij}}_{\text{Outbound transportation cost}}
\;+\;
\underbrace{\sum_{j \in D} f_j y_j}_{\text{Warehouse opening cost}}
""")

st.markdown("### Constraints")

st.latex(r"""
\sum_{j \in D} x_{ij} = 1 \quad \forall i \in C
""")

st.write("Each customer must be fully assigned to exactly one depot.")

st.latex(r"""
\sum_{i \in C} d_i x_{ij} \leq cap_j \, y_j \quad \forall j \in D
""")

st.write("Demand assigned to a depot cannot exceed its capacity unless the depot is closed.")

st.latex(r"""
x_{ij} \geq 0 \quad \text{(divisible demand)} \qquad
x_{ij} \in \{0,1\} \quad \text{(indivisible demand)}
""")

st.latex(r"""
y_j \in \{0,1\} \quad \forall j \in D
""")

st.markdown("## 3. Cost Structure Analysis")

st.write("""
To analyze the sensitivity of the network design, the model explicitly tracks inbound, outbound,
and warehouse costs as separate variables. By varying:

• transportation cost per kilometer  
• warehouse opening cost  
• the number of regional depots  

the simulator reveals how cost dominance shifts between transportation and infrastructure,
and how this impacts total system cost and facility utilization.
""")
