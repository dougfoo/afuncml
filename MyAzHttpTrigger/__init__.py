import logging

import azure.functions as func
import numpy as np
import os    
from sklearn.externals import joblib
import azureml.train.automl

models = {}
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    if (len(models) == 0):
        models['XGB2'] = joblib.load('models/sklearn_diamond_xgb_model.pkl')
        models['ISO'] = joblib.load('models/sklearn_diamond_iso_model.pkl')
        models['LR3'] = joblib.load('models/sklearn_diamond_regr_model.pkl')
        models['RF'] = joblib.load('models/sklearn_diamond_rforest_model.pkl')
        models['LBGM'] = joblib.load('models/az_automodel2.pkl')
        logging.info('(re)loaded models' + str(models))
    else:
        logging.info('loaded already: ' +str(models))

    model = req.params.get('model')
    if model:
        if (models.get(model) is None):
            print('model not found: ',model)
            return func.HttpResponse("[-1]")

        j_data = np.array(req.get_json()['data'])
        y_hat = np.array2string(models[model].predict(j_data))
        print('input: ',j_data, ', results:', y_hat)

        return func.HttpResponse(f"{y_hat}")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
