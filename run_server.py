import dill
import pandas as pd

import os

from Filds_model import Filds_model

dill._dill._reverse_typemap['ClassType'] = type

import flask

import logging

from logging.handlers import RotatingFileHandler

from time import strftime



# initialize our Flask application and the model

app = flask.Flask(__name__)

model = None



handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

logger.addHandler(handler)



def load_model(model_path):

	# load the pre-trained model

	global model

	with open(model_path, 'rb') as f:

		model = dill.load(f)



modelpath = "./Model/model_trained_XGB.dill"

load_model(modelpath)



@app.route("/", methods=["GET"])

def general():

	return """Welcome to fraudelent prediction process. Please use 'http://<address>/predict' to POST"""



filds =Filds_model.filds

@app.route("/predict", methods=["POST"])
def predict():

	data = {"success": False}

	dt = strftime("[%Y-%b-%d %H:%M:%S]")

	# ensure an image was properly uploaded to our endpoint

	if flask.request.method == "POST":

		data_pred=dict()
		data_pred.fromkeys(filds)

		request_json = flask.request.get_json()

		for fild in filds:
			data_pred[fild]=request_json[fild]


		try:
	#		csv=pd.read_csv('./Model/heart_failure_clinical_records_dataset.csv')
	#		csv.drop('DEATH_EVENT',inplace=True,axis=1)
			preds = model.predict_proba(pd.DataFrame(data_pred, index=[0]))
	#		preds = model.predict_proba(csv)


		except AttributeError as e:

			logger.warning(f'{dt} Exception: {str(e)}')

			data['predictions'] = str(e)

			data['success'] = False

			return flask.jsonify(data)



		data["predictions"] = str(preds[:, 1][0])

		# indicate that the request was a success

		data["success"] = True



	# return the data dictionary as a JSON response

	return flask.jsonify(data)

# then start the server

if __name__ == "__main__":

	print(("* Loading the model and Flask starting server..."

		"please wait until server has fully started"))

	port = int(os.environ.get('PORT', 5000))

	app.run(host='localhost', debug=True, port=port)