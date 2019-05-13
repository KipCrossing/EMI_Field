import pandas as pd

df_OpenEM = pd.read_csv("~/Cobbity/Output/Smooth_C2_OpenEM.xyz", header=None, delimiter=r"\s+")
df_DUALEM = pd.read_csv("~/Cobbity/Output/Smooth_C2_DUALEM.xyz", header=None, delimiter=r"\s+")

print(df_OpenEM.head())
print(df_DUALEM.head())
New_OpenEM_readings = []
New_OpenEM_lon = []
New_OpenEM_lat = []

sum = 0

for read in df_OpenEM[2].tolist():
    if read > -9999:
        New_OpenEM_readings.append(read)
        New_OpenEM_lon.append(df_OpenEM[0].tolist()[sum])
        New_OpenEM_lat.append(df_OpenEM[1].tolist()[sum])

    sum += 1

print(len(New_OpenEM_lon),len(New_OpenEM_lat),len(New_OpenEM_readings))

New_DUALEM_readings = []
New_DUALEM_lon = []
New_DUALEM_lat = []

sum = 0

for read in df_DUALEM[2].tolist():
    if read > -9999:
        New_DUALEM_readings.append(read)
        New_DUALEM_lon.append(df_DUALEM[0].tolist()[sum])
        New_DUALEM_lat.append(df_DUALEM[1].tolist()[sum])
    sum += 1

print(len(New_DUALEM_lon),len(New_DUALEM_lat),len(New_DUALEM_readings))

data = {"DUALEM": New_DUALEM_readings,"OpenEM": New_OpenEM_readings,"X1":New_DUALEM_lon,"X2":New_OpenEM_lon,"Y1":New_DUALEM_lat,"Y2":New_OpenEM_lat}

df_out = pd.DataFrame(data, columns=["DUALEM","OpenEM","X1","X2","Y1","Y2"])
df_out.to_csv("~/Cobbity/Output/compare_Smooth_DUALEM_OpenEm.csv")

count = 0
for i in New_DUALEM_lon:
    if New_DUALEM_lon[count] == New_OpenEM_lon[count] and New_DUALEM_lat[count] == New_OpenEM_lat[count]:
        print(count)
    count += 1


