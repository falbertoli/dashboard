# backend/h2_demand_tool.py
import pandas as pd
import numpy as np
import sqlite3


###             H2 Demand Estimation Tool           ### 
###                     SoS GC 12                   ###

def growth_rate_computation(end_year):
    growth_rate = pd.DataFrame(gr_data)
    #Percentage of flights departed from ATL that are operated by Delta
    delta_part_flights = 0.67
    #Percentage of flights operated by Delta from ATl that are domestic
    delta_part_domestic = 0.89

    ops_start = growth_rate.loc[growth_rate["Year"] == 2023, "Projected Operations"].values[0]
    ops_projected = ops_value = growth_rate.loc[growth_rate["Year"] == end_year, "Projected Operations"].values[0]
    growth = np.divide(ops_projected-ops_start,ops_start)
    growth_delta_atl = growth*delta_part_domestic*delta_part_flights
    return growth_delta_atl

def H2_demand_AC(database_name,slider_perc,end_year):
    
    #Filter the data for the Ac routes db
    conn_Ac = sqlite3.connect(database_name)
    query = """
    SELECT "AIR_TIME", "MONTH", "DATA_SOURCE", "FUEL_CONSUMPTION"
    FROM my_table
    WHERE "MONTH" = 7 AND "DATA_SOURCE" = "DU";
    """

    filtered_db = pd.read_sql(query, conn_Ac)
    conn_Ac.close()
    # Ensures every data is a number to used later
    filtered_db["AIR_TIME"] = pd.to_numeric(filtered_db["AIR_TIME"], errors='coerce')  # Convert to numbers
    filtered_db["FUEL_CONSUMPTION"] = pd.to_numeric(filtered_db["FUEL_CONSUMPTION"], errors='coerce')

     #in data, Airtime = total airtime for the month for each route, fuel consumption in lb/hr

    Fuel_weight=0
###             Block 1: Airtime flown by the selected portion of the Delta Fleet during a month            ###
    for i in range(len(filtered_db)):
        Fuel_weight += filtered_db.iloc[i,3]*filtered_db.iloc[i,0]/60 #Fuel consumption * Airtime of each route (in hr) (total airtime already in the database)
    
###             Block 2: Fuel Weight used by the selected portion of the entire Delta Fleet during a month      ###
    print("Fuel weight needed is",Fuel_weight,"lbs")

    Fuel_weight_user=slider_perc*Fuel_weight
    #Growth in operations implemented here
    growth = growth_rate_computation(end_year)
    Fuel_weight_projected = Fuel_weight_user*(1+growth)
###             Block 3: Changing mass of Jet A to mass of H2               ###
    Conv_factor = 2.8 #LHV(H2) / LHV (JetA)
    H2_weight = Fuel_weight_projected/Conv_factor # mLH2 = mjetA * 1/conversion

###             Block 4: Volume of H2 used by the selected portion of the entire Delta fleet during a month     ###
    H2_dens = 4.43 #lbs/ft3 - Departement of Energy for LH2
    H2_vol = H2_weight/H2_dens #ft3
###             Block 5 - implement the buffer margin           ###
    buffer = H2_vol/31 #demand per day in average
    H2_demand_vol = H2_vol + buffer*11 # Take eleven day of demand as a buffer - Hong Kong Airport
    print("The demand for Hydrogen for the entire month of July is", H2_demand_vol, "ft3")

###             Block 6 - Average demand per day               ###
    H2_demand_vol_day=H2_demand_vol/31
    print("The average demand for Hydrogen for one day of July is", H2_demand_vol_day, "ft3")
    
    return H2_demand_vol_day, Fuel_weight_projected

def H2_demand_GSE(database_name,GSE,end_year):
    hydrogen_tot_per_cycle = 0
    tot_Gasoline_vol_used = 0
    tot_Diesel_vol_used = 0
    #total number of operations during the month of july 2023 - includes Domestic + international - all the Airlines operating at ATL
    tot_ops_07 = 33440 
    user_input = GSE
    placeholders = ', '.join(['?'] * len(user_input))
    conn = sqlite3.connect(database_name)
    query = f"""
    SELECT 
    "Ground support Equipment", 
    "Fuel used", 
    "Usable Fuel Consumption (ft3/min)", 
    "Operating time - Departure", 
    "Operating Time - Arrival"
    FROM my_table
    WHERE "Ground support Equipment" IN ({placeholders});
    """

    file = pd.read_sql(query, conn, params=user_input)    
    conn.close()
    for i in range(len(file)):
        #All the vehicles are considered, to merge with the dashboard for selection etc 
        Fuel_vol_per_vehicle = (file.iloc[i, 2] * file.iloc[i, 3] + file.iloc[i, 2] * file.iloc[i, 4])  
        if file.iloc[i,1] == "Diesel":
            Hydrogen_volume_per_vehicle=Fuel_vol_per_vehicle/2.81
            tot_Diesel_vol_used += Fuel_vol_per_vehicle*52.283416982521 #convert ft3 in lb, denisty of diesel 52.283416982521 lb/ft3
        if file.iloc[i,1] == "Gasoline":
            Hydrogen_volume_per_vehicle=Fuel_vol_per_vehicle/2.76
            tot_Gasoline_vol_used += Fuel_vol_per_vehicle*46.3777319 #convert ft3 in lb, denisty of gasoline 46.3777319 lb/ft3

        hydrogen_tot_per_cycle += Hydrogen_volume_per_vehicle

    growth = growth_rate_computation(end_year)
    Hydrogen_tot_GSE_07 = tot_ops_07 * hydrogen_tot_per_cycle * growth
    buffer = Hydrogen_tot_GSE_07/31 
    H2_demand_vol_GSE = Hydrogen_tot_GSE_07 + buffer*11 
    daily_H2_demand_vol_GSE = H2_demand_vol_GSE/31
    return daily_H2_demand_vol_GSE, tot_Diesel_vol_used, tot_Gasoline_vol_used

# Import the data for the Ac routes & store it in a database using sqlite 
AC_data = pd.read_csv('data.csv')
conn = sqlite3.connect("Ac_data.db")
cursor = conn.cursor()
AC_data.to_sql("my_table", conn, if_exists="replace", index=False)
conn.commit()
conn.close()

# Import data for the GSE & store it in a database using sqlite 
GSE_data = pd.read_csv("Ground_fleet_data.csv", encoding_errors="ignore")
conn = sqlite3.connect("GSE_data.db")
cursor = conn.cursor()
GSE_data.to_sql("my_table", conn, if_exists="replace", index=False)
conn.commit()
conn.close()

#Growth Rate for each year in a Dataframe - TAF data
gr_data = {
    "Year": list(range(2023, 2051)),
    "Projected Operations": [
        755856, 784123, 815016, 834644, 853350, 872286, 890251, 
        907846, 925298, 942989, 960976, 979187, 997398, 1016764, 
        1036063, 1055234, 1074792, 1094786, 1114237, 1134615, 1155514, 
        1176625, 1197973, 1219542, 1241334, 1263264, 1285643, 1308659
    ]
}
#First try - to prove that it works
end_year = 2036

slider_percentage = 0.1
nom = "Ac_data.db"

vol, tot_jetA = H2_demand_AC(nom,slider_percentage,end_year)
print(vol)

GSE_entry = ["F250","F650_1"]
nom2 = "GSE_data.db"
vol_GSE, vol_Diesel, vol_Gasoline = H2_demand_GSE(nom2,GSE_entry,end_year)
print(vol_GSE)

###             Tank specification              ###
tank_width = 10.1667 #ft
tank_length = 56.5 #ft
Water_cap = 18014/7.48052 #gal->ft3
Tank_ullage = 0.05 #% of volume taken by gas form of H2 in the tank - Assumed using Argonne study
evaporation = 99.25 #% of LH2 lost per day - Use Specification for tank
tank_H2_storage = Water_cap*(1-Tank_ullage)*evaporation


def storage_area(H2_demand_vol):
###             Block 7 - Total Area taken by the storage of the H2 demand              ###
    nbr_tanks = H2_demand_vol/tank_H2_storage
    area_tank = tank_width*tank_length
    area_tot=area_tank*nbr_tanks #ft2
    print("The total area taken to store this hydrogen is", area_tot, "ft2")
    return area_tot


def emissions_fuels(tot_jetA,tot_diesel,tot_Gasoline):
    #Emissions factors from EPA - Greenhouse Gas Emissions from a Typical Passenger Vehicle
    jetA_emission_factor = 9.57 #kg CO2/lb Jet A, mock value from chatgpt
    diesel_emission_factor = 22.38 #kg CO2/lb Diesel, mock value from chatgpt
    gasoline_emission_factor = 19.64 #kg CO2/lb Gasoline, mock value from chatgpt

    jetA_emissions = tot_jetA * jetA_emission_factor
    diesel_emissions = tot_diesel * diesel_emission_factor
    gasoline_emissions = tot_Gasoline * gasoline_emission_factor

    total_emissions = jetA_emissions + diesel_emissions + gasoline_emissions

    print("Total CO2 emissions from Jet A, Diesel, and Gasoline are", total_emissions, "kg")
    return total_emissions

tot_emissions_try = emissions_fuels(tot_jetA, vol_Diesel, vol_Gasoline)