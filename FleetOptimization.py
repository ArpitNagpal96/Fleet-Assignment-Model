import gurobipy as gp
from gurobipy import *
import numpy as np
import pandas as pd

df_routes=pd.read_excel('Flight_Routes_Data_F.xlsx')

df_routes['Defined_Leg']=df_routes['Origin']+"_"+df_routes['Destination']
df_routes

df_routes['Total Revenue']=df_routes['Number of Passengers']*df_routes['Fares']

df_fleet=pd.read_csv(r'fleet_capacity.csv')
df_cost=pd.read_excel(r'Flights_Cost_Data_Final.xlsx')

model=gp.Model('Airline Fleet Assignment')

fleet_list=list(df_fleet['Fleet'].unique())
route_list=list(df_routes['Defined_Leg'])

fleet_assignment = model.addMVar((len(route_list),len(fleet_list)),vtype=GRB.BINARY,lb=0, name = ["x_"+i+"_"+j for i in route_list for j in fleet_list])
y = model.addMVar((len(set(df_routes['Origin'])),len(fleet_list)),vtype=GRB.INTEGER,lb=0, name = ["y_"+i+"_"+j for i in set(df_routes['Origin']) for j in fleet_list])

v=0
fleet_assignment_costs=np.zeros(((len(route_list)), (len(fleet_list))))
for i in range(len(route_list)):
    for j in range(len(fleet_list)):
        print(i,j)
        fleet_assignment_costs[i][j]=df_cost['Total Cost'].iloc[v]
        v=v+1

#total_profit_calculation = sum(fleet_assignment[i][j]*(df_routes['Total Revenue'][i]-fleet_assignment_costs[i][j]) for i in range(len(route_list)) for j in range(len(fleet_list)))
total_profit_calculation = sum(fleet_assignment[i][j]*fleet_assignment_costs[i][j] for i in range(len(route_list)) for j in range(len(fleet_list)))

model.setObjective(total_profit_calculation, GRB.MINIMIZE)

fleet_capacity=df_fleet['Capacity']
for i in range(len(route_list)):
    model.addConstr(sum(fleet_assignment[i][j] for j in range(len(fleet_list)))==1,name='Coverage Constraint')
    model.addConstr(sum(fleet_assignment[i][j]*fleet_capacity[j] for j in range(len(fleet_list)))>=df_routes['Number of Passengers'][i],name='Resource to Demand Constraint')
    #Overbooking cancellation and spillage cost


for j in range(len(fleet_list)):
    #model.addConstr(sum(y[i][j] for i in range(len(set(df_routes['Origin']))) for j in range(len(fleet_list)))+sum(fleet_assignment[i][j]-y[i][j] for i in range(len(route_list)) for j in range(len(fleet_list)) if route_list[i] in set(df_routes['Origin']))-sum(fleet_assignment[i][j] for i in range(len(route_list)) for j in range(len(fleet_list)) if route_list[i] in set(df_routes['Destination']))==0)
    model.addConstr(sum(y[i][j] for i in range(len(set(df_routes['Origin']))))+sum(fleet_assignment[i][j]-y[i][j] for i in range(len(route_list)) if route_list[i] in set(df_routes['Origin']))-sum(fleet_assignment[i][j] for i in range(len(route_list)) if route_list[i] in set(df_routes['Destination']))==0)


origin_list=list(df_routes['Origin'].unique())
destination_list=list(df_routes['Destination'].unique())

model.optimize()

#origin_list

model.getVars()

#destination_list

from datetime import datetime
for i in range(len(df_routes)):
    for j in range(len(df_routes)):
        if df_routes['Destination'][i]==df_routes['Origin'][j]:
            end=datetime.strptime(str(df_routes['departure_time'][j]),"%H:%M:%S")
            start=datetime.strptime(str(df_routes['arrival_time'][i]),"%H:%M:%S")
            if end>start:
                print("Coming from "+df_routes['Origin'][i]+" arriving at "+df_routes['Destination'][i]+" leaving to "+df_routes['Destination'][j]+" after:"+str(end-start))   

from datetime import datetime, timedelta
for i in range(len(df_routes)):
    ground_halts=[]
    for j in range(len(df_routes)):
        if df_routes['Destination'][i]==df_routes['Origin'][j] and i!=j:
            end=datetime.strptime(str(df_routes['departure_time'][j]),"%H:%M:%S")
            start=datetime.strptime(str(df_routes['arrival_time'][i]),"%H:%M:%S")
            ground_halts.append(end-start)
    for k in range(len(ground_halts)):
        if (ground_halts[k]>=timedelta(hours=3)) and (ground_halts[k]<=timedelta(hours=6)):
            for z in range(len(df_fleet)):
                model.addConstr(fleet_assignment[i][z]==fleet_assignment[j][z], name="Through Flights Constraint")
        if (ground_halts[k]>=timedelta(hours=3)) and (ground_halts[k]<=timedelta(hours=6)):
            for z in range(len(df_fleet)):
                model.addConstr(fleet_assignment[i][z]==fleet_assignment[j][z], name="Through Flights Constraint")        

df_routes

flight_list=[]
ground_list=[]
import datetime

def time_in_range(start, end, current):
    return start <= current <= end
from datetime import datetime, timedelta
flight_arc=0
ground_arc=0
time_arc_1 =datetime.strptime(str("18:00:00"),'%H:%M:%S')
time_arc=datetime.time(time_arc_1)
for l in range(len(df_routes)):
    start=datetime.strptime(str(df_routes.iloc[l]['departure_time']),"%H:%M:%S")
    end=datetime.strptime(str(df_routes.iloc[l]['arrival_time']),"%H:%M:%S")
    start_time = datetime.time(start)
    end_time = datetime.time(end)
    if(time_in_range(start_time, end_time, time_arc)):
        flight_arc+=1
        flight_list.append(df_routes.iloc[l]['Defined_Leg'])
    else:
        ground_arc+=1
        ground_list.append(df_routes.iloc[l]['Origin'])
    model.addConstr(flight_arc+ground_arc<=len(df_routes))

for a in range(len(df_fleet)):
    model.addConstr((sum(y[i][a] for i in range(len(set(ground_list))))+sum(fleet_assignment[i][a] for i in range(len(flight_list))))<=df_fleet['Number of Aircrafts'][a])


set(ground_list)

flight_arc+ground_arc

model.getVars()

for i in range(len(df_routes)):
    incoming_sum=[0,0,0]
    outgoing_sum=[0,0,0]
    for k in range(len(df_fleet)):
        for j in range(len(df_routes)):
            if df_routes['Destination'][i]==df_routes['Destination'][j] and i!=j:
                incoming_sum[k]+=fleet_assignment[j][k]
    for k in range(len(df_fleet)):
        for a in range(len(df_routes)):
            if df_routes['Destination'][i]==df_routes['Origin'][a] and i!=a:
                outgoing_sum[k]+=fleet_assignment[a][k]
    for n in range(len(df_fleet)):
        model.addConstr(incoming_sum[n]==outgoing_sum[n],name='Airport(node) Traffic Balancing Constraint')

model.optimize()

model.getVars()

import matplotlib.pyplot as plt
list_varname=[]
list_values=[]
sum_73w=0
sum_e75=0
sum_dh4=0
for v in model.getVars():
    #print('%s %g' % (v.varName, v.x))
    list_varname.append(v.varName)
    list_values.append(v.x)
    if('73W' in v.varName):
        sum_73w+=v.x
    if('E75' in v.varName):
        sum_e75+=v.x
    if('DH4' in v.varName):
        sum_dh4+=v.x
list_dict=dict(list(zip(list_varname,list_values)))
keys = list_dict.keys()
values = list_dict.values()
#plt.bar(keys, values)
#plt.show()
sum_73w,sum_e75,sum_dh4

