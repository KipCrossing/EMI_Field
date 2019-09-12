# this codd combinds the GPS data with the OpenEM data
import pandas as pd

gps_df = pd.read_csv('CobbityGPS_10am.csv')
openem_df = pd.read_csv('Cobbity9_run1.csv')
print(list(openem_df))
output_df = gps_df

# ID,Amp,Shift,Shift_out,Voltage,Temp,Humidity,Hs,Hp
output_df['Amp'] = output_df['ID']
output_df['Shift'] = output_df['ID']
output_df['Voltage'] = output_df['ID']
output_df['Temp'] = output_df['ID']
output_df['Humidity'] = output_df['ID']
output_df['Hs'] = output_df['ID']
output_df['Hp'] = output_df['ID']
output_df['Adj'] = output_df['ID']

print(output_df.head())

for id_i in range(len(gps_df['ID'])):
    for id_j in range(len(openem_df['ID'])):
        if gps_df['ID'][id_i] == openem_df['ID'][id_j]:
            output_df['Amp'][id_i] = openem_df['Amp_rolling'][id_j]
            output_df['Shift'][id_i] = openem_df['Shift'][id_j]
            output_df['Voltage'][id_i] = openem_df['Volt_rolling'][id_j]
            output_df['Temp'][id_i] = openem_df['Temp_rolling'][id_j]
            output_df['Humidity'][id_i] = openem_df['Humidity'][id_j]
            output_df['Hs'][id_i] = openem_df['Hs_rolling'][id_j]
            output_df['Hp'][id_i] = openem_df['Hp_rolling'][id_j]
            output_df['Adj'][id_i] = openem_df['Adj'][id_j]


output_df.to_csv('OpenEM_Cobbity_10am_all.csv', index=False)
