import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
pluvData = pd.read_csv("pluvdata.csv")
callData = pd.read_csv("call1746.csv")

# Remove absurd data
pluvData.drop(pluvData.index[pluvData["acumulado_chuva_4_h"] > 200], axis="index", inplace=True)

# Remove NaN
pluvData.dropna(axis="index", inplace=True)
callData.dropna(axis="index", inplace=True)

# Merge time related columns of pluvData and set the result as the index
mergedTime = pluvData.loc[:, "data_particao"] + "T" + pluvData.loc[:, "horario"]
mergedTime.name = "tempo"
pluvData.index = mergedTime.apply(np.datetime64)
pluvData.drop(["horario", "data_particao", "id_estacao"], axis="columns", inplace=True)

# Set time column as index for callData
timeColumn = callData.loc[:, "data_inicio"]
timeColumn.name = "tempo"
callData.index = timeColumn.apply(np.datetime64)
callData.drop(["data_inicio"], axis="columns", inplace=True)

# Take the average of the stations at each timestamp
pluvData = pluvData.groupby("tempo").mean()

# Sort each data frame by time in a descending order
callData.sort_index(ascending=False, inplace=True)
pluvData.sort_index(ascending=False, inplace=True)

# Calculate the rolling count of calls
#callData = callData.loc[callData["id_tipo"] == 9]
callData = callData.rolling('24H').count()
callData.columns = ["contagem_chamadas"]
callData -= 1

mindate = np.datetime64("2023-02-01")
maxdate = np.datetime64("2024-02-29")

pluvRange = np.logical_and((pluvData.index > mindate), (pluvData.index < maxdate))
callRange = np.logical_and((callData.index > mindate), (callData.index < maxdate))

pluvData = pluvData.iloc[pluvRange]
callData = callData.iloc[callRange]

callData.sort_index(ascending=True, inplace=True)
pluvData.sort_index(ascending=True, inplace=True)

print(pluvData)
print(callData)

matchedData = pd.merge_asof(callData, pluvData, "tempo", direction="nearest")
matchedData.index = matchedData["tempo"]
matchedData.drop(["tempo"], axis="columns", inplace=True)
matchedData.sort_index(ascending=False, inplace=True)
print(matchedData)

callData.sort_index(ascending=False, inplace=True)
pluvData.sort_index(ascending=False, inplace=True)
#sns.lineplot(pluvData.loc[:, ["acumulado_chuva_15_min", "acumulado_chuva_4_h", "acumulado_chuva_24_h"]], palette="flare")
#sns.lineplot(callData.loc[:, ["contagem_chamadas"]], palette="mako_r")
#plt.show()

sns.regplot(matchedData, x="acumulado_chuva_24_h", y="contagem_chamadas")
plt.show()
