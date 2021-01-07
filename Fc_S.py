import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

num_episode = 5
fig = plt.figure(figsize = (14,8))

for i in range(0, num_episode):
    df = pd.read_csv(f"phase_diagram{i}.csv")
    df_pivot = df.pivot('Pr','r', 'Fc_S')
    ax = fig.add_subplot(2, 5, i+1)
    sns.heatmap(df_pivot,
                vmin = 0.0, 
                vmax = 1.0, 
                annot = False, 
                cbar = True,
                cmap ="jet",
                square = True,
                xticklabels = 4,
                yticklabels = 4)
    ax.set_title(f"Episode{i}")

    
plt.tight_layout()
fig.suptitle('Fraction of Honest Seller')
fig.savefig('Pr-r-Fc_S_Diagram.png')

