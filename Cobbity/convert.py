import pandas as pd
import numpy as np

df_OpenEM = pd.read_csv("~/Cobbity/logs/OpenReadings.csv")
df_GPS = pd.read_csv("~/Cobbity/logs/open_em_gps")


DateTimes = df_OpenEM["Time "].tolist()
Lon = df_OpenEM["Longitude"].tolist()
Lat = df_OpenEM["Latitude"].tolist()
Readings = df_OpenEM["Reading"].tolist()


cut = 155
Longitude = df_GPS["WGS84_LON"].tolist()[cut:-316]
Latitude = df_GPS["WGS84_LAT"].tolist()[cut:-316]

acc_time = []
acc_lon = []
acc_lat = []
acc_readings = Readings[:-1]

sum = 0

secondtimes = []

for datetime in DateTimes:
    time = datetime[11:20]
    hour = int(time[0:2])
    min = int(time[3:5])
    sec = int(time[6:])
    secondtime = sec + min*60 + hour*60*60-52343
    secondtimes.append(secondtime)




for thetime in df_GPS["GPS_TIME"].tolist()[cut:-316]:

    for OpenTime in secondtimes:

        if OpenTime == sum:
            #print("YES: " + str(OpenTime))
            acc_time.append(sum)
            acc_lon.append(Longitude[sum])
            acc_lat.append(Latitude[sum])
    sum += 1
print(len(acc_time))
print(len(acc_lon))
print(len(acc_lat))
print(len(acc_readings))
data = {"Time": acc_time, "Lon" : acc_lon, "Lat" : acc_lat,"Reading":acc_readings}



df_accurate_gps = pd.DataFrame(data, columns=["Time", "Lon", "Lat","Reading"])

df_accurate_gps.to_csv("Combined_OpenEM_GPS.csv")

df_C1 = df_accurate_gps[:83]
df_C1.to_csv("C1_OpenEM_GPS.csv")
df_C2 = df_accurate_gps[130:348]
df_C2.to_csv("C2_OpenEM_GPS.csv")



##########-----------##########-----------##########








#print(secondtimes)

Readings_Rounded = []
for Reading in Readings:
    Readings_Rounded.append(round(float(Reading),6))

data2 = {"Time":secondtimes,"Lon":Lon,"Lat":Lat,"Reading":Readings_Rounded}

df_Open_new = pd.DataFrame(data2, columns=["Time", "Lon", "Lat", "Reading"])
df_Open_new.to_csv("OpenEm_new.csv")

Readings_Rounded


