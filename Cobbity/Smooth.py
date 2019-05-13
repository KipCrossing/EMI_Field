import numpy as np

import pandas as pd

from scipy.ndimage.filters import gaussian_filter



df_OpenEM = pd.read_csv("~/Cobbity/logs/dualem_C1.csv")
print(df_OpenEM.head())


data_list = df_OpenEM["Reading5"].tolist()
time_list = df_OpenEM["Time"].tolist()
lon_list = df_OpenEM["Lon"].tolist()
lat_list = df_OpenEM["Lat"].tolist()

blurred = gaussian_filter(data_list, sigma=1)
print(len(data_list))
print(len(blurred))


data = {"Time": time_list, "Lon": lon_list, "Lat":lat_list,"Reading":data_list}

df_out = pd.DataFrame(data, columns=["Time", "Lon", "Lat","Reading"])

print(df_out.head())

#df_out.to_csv("Smoothed_Dualem1.csv")


def rolling_ave(array1D, radius = 5):
    count = 0
    out_array = []
    for i in array1D:

        if count > radius and count < len(array1D)-radius:

            sum = 0
            for k in range(radius*2):
                print(count,k)
                sum += array1D[count - radius + k]
            out_array.append(sum/(radius*2))

        else:
            out_array.append(i)
        count +=1
    return out_array

print(len(rolling_ave(data_list)))


data = {"Time": time_list, "Lon": lon_list, "Lat":lat_list,"Reading":rolling_ave(data_list,5)}

df_out = pd.DataFrame(data, columns=["Time", "Lon", "Lat","Reading"])

print(df_out.head())

df_out.to_csv("Smoothed_Dualem_C1.csv")

