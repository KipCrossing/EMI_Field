import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('OpenData_20190904_140038.csv')

print(list(df))
count = 0
for id_i in range(1, len(df['ID'])-1):
    if not (df['ID'][id_i+1] < df['ID'][id_i] + 200 and df['ID'][id_i+1] > df['ID'][id_i]):
        df['ID'][id_i+1] = df['ID'][id_i] + 1
        count += 1

print(count)

# plt.plot(df['Longitude'])
plt.plot(df['ID'])
plt.show()

df.to_csv('CobbityGPS_2pm.csv', index=False)
