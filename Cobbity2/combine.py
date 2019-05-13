 
import pandas as pd

# "~/Cobbity/logs/kip_dulaule"
# "~/Cobbity/logs/dualem_full.csv"


df_OpenEm = pd.read_csv("OpenEmRunKip.csv")
OpenHeading = list(df_OpenEm)
df_GPS = pd.read_csv("GPSopenEM.csv")
gpsHeading = list(df_GPS)


tsum = 0

output = [] 

for i in range(0,len(gpsHeading)-1):
    output.append([])

for i in OpenHeading:
    output.append([])
    
for i in range(len(df_OpenEm["S16"])):
    
    if round(df_OpenEm["S16"][i],3) == round(df_GPS["Reading"][i-tsum],3):
        output[0].append(df_GPS["Latitude"][i-tsum])
        output[1].append(df_GPS["Longitude"][i-tsum])
        output[2].append(df_GPS["Accuracy"][i-tsum])
        output[3].append(df_GPS["Time"][i-tsum])
        
        output[4].append(df_OpenEm["ID"][i])
        for j in range(len(OpenHeading)-1):
            output[j+5].append(round(df_OpenEm["S"+str(j+1)][i],2))
        
        
            #output[21].append(round(df_OpenEm["S16"][i],2))
            #output[22].append(round(df_OpenEm["S17"][i],2))
        #print(i+2,i-tsum+2)
    else:
        tsum += 1

data_full = []

for i in range(0,len(gpsHeading)-1):
    data_full.append((gpsHeading[i],output[i]))
    
for i in range(0,len(OpenHeading)):
    data_full.append((OpenHeading[i],output[i+4]))



data_full = (dict(data_full))

#print(output[3])



gpsHeading.pop(4)

outHeading = gpsHeading + OpenHeading
print(len(outHeading),len(output))

df_out = pd.DataFrame(data_full,columns=outHeading)

df_out.to_csv("Combined.csv")


#print("output to: "+outputfile)

