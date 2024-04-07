import pandas
import os
data1 = pandas.read_csv("1D_All_ReplaysData_PvP.csv")
data2 = pandas.read_csv("1D_All_ReplaysData_PvT.csv")
data3 = pandas.read_csv("1D_All_ReplaysData_PvZ.csv")
data4 = pandas.read_csv("1D_All_ReplaysData_TvZ.csv")
data5 = pandas.read_csv("1D_All_ReplaysData_TvT.csv")
data6 = pandas.read_csv("1D_All_ReplaysData_ZvZ.csv")
# combine all data and add the columns and set as 0 if not present

data = pandas.concat([data1, data2, data3,data4, data5, data6], sort=False)
data = data.fillna(0)

data.to_csv("StarCraft_Combined_Dataset.csv", index=False)