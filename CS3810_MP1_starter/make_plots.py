import pandas as pd
import matplotlib.pyplot as plt

"""df = pd.read_csv('C:/Users\jayde/CS-3810/CS3810_MP1_starter/results.csv')

# Filter to the rows you want
astar = df[df['algorithm'] == 'astar']

# Group and plot
for h in ['h0', 'h1', 'h2', 'h3']:
    subset = astar[astar['heuristic'] == h]
    plt.plot(subset['n_dirty'], subset['nodes_expanded'], marker='o', label=h)

plt.xlabel('Number of dirty cells')
plt.ylabel('Nodes expanded')
plt.title('A* nodes expanded by heuristic')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('figures/astar_heuristics.png', dpi=150, bbox_inches='tight')
plt.close()"""

df = pd.read_csv('results.csv')

# Keep only the IDA* rows
idastar = df[df['algorithm'] == 'idastar']

plt.figure(figsize=(8, 5))

for h in ['h0', 'h1', 'h2', 'h3']:
    subset = idastar[idastar['heuristic'] == h]
    plt.plot(subset['n_dirty'], subset['iterations'],
             marker='o', label=h)

plt.xlabel('Number of dirty cells')
plt.ylabel('Iterations')
plt.title('IDA* iterations by heuristic')
plt.legend(title='Heuristic')
plt.grid(True, alpha=0.3)
plt.savefig('figures/idastar_iterations.png', dpi=150, bbox_inches='tight')
plt.close()

print("Saved figures/idastar_iterations.png")