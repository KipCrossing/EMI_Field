import pandas as pd

# "~/Cobbity/logs/kip_dulaule"
# "~/Cobbity/logs/dualem_full.csv"

def dualem(inputfile, outputfile = "output.csv"):
    df_DUALEM = pd.read_csv(inputfile)


    sum = 0

    time = []
    lon = []
    lat = []
    readings1 = []
    readings2 = []
    readings3 = []
    readings4 = []
    readings5 = []
    readings6 = []
    readings7 = []
    readings8 = []

    for Lon in df_DUALEM["WGS84_LON"]:
        if str(Lon) != "nan":
            print(round(Lon,8),round(df_DUALEM["WGS84_LAT"][sum],8),round(df_DUALEM["AUX_X3"][sum+1],5))
            time.append(sum)
            lon.append(round(Lon,8))
            lat.append(round(df_DUALEM["WGS84_LAT"][sum],8))
            readings1.append(round(df_DUALEM["AUX_X2"][sum+1],5))   #1m HCP con
            readings2.append(round(df_DUALEM["AUX_X2"][sum+2],5))   #2m HCP con
            readings3.append(round(df_DUALEM["AUX_X3"][sum+1],5))   #1m HCP in
            readings4.append(round(df_DUALEM["AUX_X3"][sum+2],5))   #2m HCP in
            readings5.append(round(df_DUALEM["AUX_X4"][sum+1],5))   #1m PRP con
            readings6.append(round(df_DUALEM["AUX_X4"][sum+2],5))   #2m PRP con
            readings7.append(round(df_DUALEM["AUX_X5"][sum+1],5))   #1m PPR in
            readings8.append(round(df_DUALEM["AUX_X5"][sum+2],5))   #2m PPR in
        sum += 1


    data_full = {"Time": time,"Lon":lon,"Lat":lat,"1mHCPcon":readings1,"2mHCPcon":readings2,"1mHCPmag":readings3,"2mHCPmag":readings4,"1mPRPcon":readings5,"2mPRPcon":readings6,"1mPRPmag":readings7, "2mPRPmag":readings8}

    df_out = pd.DataFrame(data_full,columns=["Time","Lon","Lat","1mHCPcon","2mHCPcon","1mHCPmag","2mHCPmag","1mPRPcon","2mPRPcon","1mPRPmag","2mPRPmag"])

    df_out.to_csv(outputfile)

    print("output to: "+outputfile)
