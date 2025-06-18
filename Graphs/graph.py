import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.patches import Patch

# Load Excel data
file_path = r"C:\Users\pnish\Desktop\erf-oddo.xlsx"
df = pd.read_excel(file_path)

# Clean and map data
df = df[df['Surface Location'].isin(['Internal', 'External'])].copy()
df.sort_values(by='Abs. Distance (m)', inplace=True)
df['y'] = df['Surface Location'].map({'Internal': 0, 'External': 1})
df['x_index'] = np.arange(len(df))

# Graph data
x = df['x_index'].values
y = df['y'].values
z = np.zeros_like(x)
dx = np.ones_like(x)
dy = np.ones_like(x)
dz = df['ERF (ASME B31G)'].values
colors = ['steelblue' if val == 'Internal' else 'orangered' for val in df['Surface Location']]

# Create figure
fig = plt.figure(figsize=(18, 8))
ax = fig.add_subplot(111, projection='3d')
ax.bar3d(x, y, z, dx, dy, dz, color=colors, shade=True)

# More frequent x-ticks: 25 evenly spaced
tick_count = 25
tick_positions = np.linspace(0, len(df) - 1, tick_count, dtype=int)
tick_labels = df['Abs. Distance (m)'].iloc[tick_positions].round(0).astype(int).astype(str).values
ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_labels, rotation=45, ha='right')

# Y-ticks
ax.set_yticks([0, 1])
ax.set_yticklabels(['Internal', 'External'])

# Axis labels
ax.set_xlabel('Distance from Launcher (ODDO)', labelpad=15)
ax.set_ylabel('Surface Type', labelpad=10)
ax.set_zlabel('ERF (ASME B31G)', labelpad=10)
ax.set_title('ERF vs ODDO for Internal & External Defects', pad=20)

# Legend
legend_elements = [
    Patch(facecolor='steelblue', edgecolor='k', label='Internal'),
    Patch(facecolor='orangered', edgecolor='k', label='External')
]
ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0.02, 0.95))

plt.tight_layout()
plt.show()