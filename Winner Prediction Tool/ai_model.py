from joblib import dump, load
import os 
import pandas as pd
estimator = load('C:/Users/abhin/Documents/HW University/Dissertation/UI App/Tool_Final/simple_random_forest_model.joblib')
estimator2 = load('C:/Users/abhin/Documents/HW University/Dissertation/UI App/Tool_Final/gameState_random_forest_model.joblib')

def predict_simple(data):
    print(data)
    req_data = data[0:-2]
    # return estimator.predict_proba(data)
    req_data[0] = convertRace(req_data[0])
    req_data[1] = convertRace(req_data[1])
    #convert into pandas dataframe
    data = pd.DataFrame([req_data], columns= ["Player1_Race","Player2_Race","Player1_AliveUnits","Player2_AliveUnits","Player1_SupplyUsed","Player2_SupplyUsed","Player1_Gas","Player2_Gas", "Player1_Minerals", "Player2_Minerals"])
    print(data)

    #predict the winner
    result = estimator.predict_proba(data)
    print(result[0].tolist())

    return result[0].tolist()

def predict_gameState(data):
    print(data)
    req_data = data[0:-2]
    # return estimator.predict_proba(data)
    req_data[0] = convertRace(req_data[0])
    req_data[1] = convertRace(req_data[1])
    #convert into pandas dataframe
    data = pd.DataFrame([req_data], columns= ['Player1_Race','Player2_Race','MapName','MapWidth', 'MapHeight', 'Player1_EAPM', 'Player2_EAPM', 'Player1_ECmdCount', 'Player2_ECmdCount', 'Player1_TotalUnits', 'Player2_TotalUnits', 'Player1_AliveUnits', 'Player2_AliveUnits'])
    print(data)

    #predict the winner
    result = estimator2.predict_proba(data)
    print(result[0].tolist())

    return result[0].tolist()

def convertRace(val):
    if val == 'Protoss':
        return 0
    elif val == 'Terran':
        return 1
    else:
        return 2

d = ['Terran', 'Zerg', '10', '20', '100', '200', '50', '100', '100', '200', "100" ,"200"]
d2 = ['Protoss', 'Protoss', '1', '1', '11', '1', '11', '1', '1', '1', '1', '1', '2','1', '2']
#predict_simple(d)

predict_gameState(d2)