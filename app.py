import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="TSP Visualisation", layout="centered")

st.title("Travelling Salesman Problem (TSP) Visualisation")

# ------------------------------
# 1. User input
# ------------------------------
n_cities = st.number_input(
    "Number of cities",
    min_value=2,
    max_value=200,
    value=10,
    step=1
)

# ------------------------------
# 2. Generate random coordinates
# ------------------------------
cities = np.random.rand(n_cities, 2)

# ------------------------------
# 3. Compute distance matrix
# ------------------------------
dist_matrix = np.sqrt(((cities[:, np.newaxis, :] - cities[np.newaxis, :, :]) ** 2).sum(axis=2))

st.subheader("Distance matrix")
# Display the full distance matrix in a scrollable table
st.dataframe(pd.DataFrame(dist_matrix).round(3), width=600, height=300)

# ------------------------------
# 4. Solve TSP (nearest neighbour)
# ------------------------------
def nearest_neighbour(cities):
    n = len(cities)
    unvisited = list(range(n))
    path = [unvisited.pop(0)]
    while unvisited:
        last = path[-1]
        next_city = min(unvisited, key=lambda city: np.linalg.norm(cities[last]-cities[city]))
        path.append(next_city)
        unvisited.remove(next_city)
    return path

path = nearest_neighbour(cities)

# Compute total path length
total_length = sum(
    np.linalg.norm(cities[path[i]] - cities[path[(i + 1) % n_cities]]) for i in range(n_cities)
)
st.write(f"Total path length (nearest neighbour heuristic): {total_length:.3f}")

# ------------------------------
# 5. Plot TSP path with black background
# ------------------------------
fig, ax = plt.subplots(figsize=(6, 4), facecolor='black')  # smaller figure
ax.set_facecolor('black')

# Plot cities
ax.scatter(cities[:, 0], cities[:, 1], c='cyan', s=50, zorder=2, label="Cities")

# Plot path
for i in range(len(path)):
    start = cities[path[i]]
    end = cities[path[(i + 1) % n_cities]]  # wrap around
    ax.plot([start[0], end[0]], [start[1], end[1]], 'magenta', lw=1.5, zorder=1)

# Styling
ax.set_title("TSP Path using Nearest Neighbour", color='white')
ax.tick_params(colors='white')
for spine in ax.spines.values():
    spine.set_color('white')
ax.legend(facecolor='black', labelcolor='white')

st.pyplot(fig)
