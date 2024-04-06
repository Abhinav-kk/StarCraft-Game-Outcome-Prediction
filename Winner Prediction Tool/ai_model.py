from joblib import dump, load
import os 
import pandas as pd
estimator = load(os.getcwd() + '/models/simple_random_forest_model.joblib')
estimator2 = load(os.getcwd() + '/models/gameState_random_forest_model.joblib')
estimator3 = load(os.getcwd() + '/models/simple_svm_model.joblib')
estimator4 = load(os.getcwd() + '/models/gameState_svm_model.joblib')
estimator5 = load(os.getcwd() + '/models/simple_LR_model.joblib')
estimator6 = load(os.getcwd() + '/models/gameState_LR_model.joblib')
estimator7 = load(os.getcwd() + '/models/simple_KNN_model.joblib')
estimator8 = load(os.getcwd() + '/models/gameState_KNN_model.joblib')
estimator9 = load(os.getcwd() + '/models/simple_DT_model.joblib')
estimator10 = load(os.getcwd() + '/models/gameState_DT_model.joblib')

def predict_simple(data,model):
    print(data)
    req_data = data[0:-2]
    # return estimator.predict_proba(data)
    req_data[0] = convertRace(req_data[0])
    req_data[1] = convertRace(req_data[1])
    #convert into pandas dataframe
    data = pd.DataFrame([req_data], columns= ["Player1_Race","Player2_Race","Player1_AliveUnits","Player2_AliveUnits","Player1_SupplyUsed","Player2_SupplyUsed","Player1_Gas","Player2_Gas", "Player1_Minerals", "Player2_Minerals"])
    print(data)

    print("model",model)

    if model == "Random Forest":
        model = estimator
        result = model.predict_proba(data)
    elif model == "Support Vector Classification":
        model = estimator3
        result = model._predict_proba_lr(data)
    elif model == "Logistic Regression":
        model = estimator5
        result = model.predict_proba(data)
    elif model == "K-Nearest Neighbors":
        model = estimator7
        result = model.predict_proba(data)
    elif model == "Decision Trees":
        model = estimator9
        result = model.predict_proba(data)
    else:
        return [0,0]

    print(result[0].tolist())
    #predict the winner
    result = [ round(i*100,2) for i in result[0].tolist() ]
    return result

def predict_gameState(data,model):
    print(data)
    req_data = data[0:-2]
    # return estimator.predict_proba(data)
    req_data[0] = convertRace(req_data[0])
    req_data[1] = convertRace(req_data[1])
    #convert into pandas dataframe
    data = pd.DataFrame([req_data], columns= ['Player1_Race','Player2_Race','MapName','MapWidth', 'MapHeight', 'Player1_EAPM', 'Player2_EAPM', 'Player1_ECmdCount', 'Player2_ECmdCount', 'Player1_TotalUnits', 'Player2_TotalUnits', 'Player1_AliveUnits', 'Player2_AliveUnits'])
    print(data)

    if model == "Random Forest":
        model = estimator2
        result = model.predict_proba(data)
    elif model == "Support Vector Classification":
        model = estimator4
        result = model._predict_proba_lr(data)
    elif model == "Logistic Regression":
        model = estimator6
        result = model.predict_proba(data)
    elif model == "K-Nearest Neighbors":
        model = estimator8
        result = model.predict_proba(data)
    elif model == "Decision Trees":
        model = estimator10
        result = model.predict_proba(data)
    else:
        return [0,0]

    #predict the winner
    print(result[0].tolist())
    result = [ round(i,2) for i in result[0].tolist() ]
    return result

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

predict_gameState(d2,"random")