import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# openem_df = pd.read_csv("OpenEM_Cobbity_10am_straight.csv")
openem_df = pd.read_csv("OpenEM_Cobbity_2pm_straight.csv")

print(list(openem_df))
Hs_adj = openem_df['Hs'] - openem_df['Temp']*2500-63000
plt.plot(openem_df['ID'], Hs_adj)
plt.plot(openem_df['ID'], openem_df['Hs'])
plt.show()
plt.scatter(openem_df['Longitude'], openem_df['Latitude'], c=openem_df['Hp'])
plt.ylim(openem_df['Latitude'].min(), openem_df['Latitude'].max())
plt.xlim(openem_df['Longitude'].min(), openem_df['Longitude'].max())
plt.show()
