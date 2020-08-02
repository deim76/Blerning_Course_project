

from urllib import request, parse

import urllib.request

import json



def get_prediction(data_pred):

    myurl = "http://localhost:5000/predict"

    req = urllib.request.Request(myurl)

    req.add_header('Content-Type', 'application/json; charset=utf-8')

    jsondata = json.dumps(data_pred)

    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes

    req.add_header('Content-Length', len(jsondataasbytes))

    response = urllib.request.urlopen(req, jsondataasbytes)

    return json.loads(response.read())['predictions']



if __name__=='__main__':

    description = '''\xa0'''

    data_pred = {'age':75.0,
            'anaemia':0,
            'creatinine_phosphokinase':582,
            'diabetes':0,
            'ejection_fraction':45,
            'high_blood_pressure':1,
            'platelets':263358.03,
            'serum_creatinine':1.18,
            'serum_sodium':137,
            'sex':1,
            'smoking':0,
            'time':4}




    preds = get_prediction(data_pred)

    print(preds)