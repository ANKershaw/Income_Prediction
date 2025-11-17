"""
This script will include:
	Loading the model
	Serving it via a web service (with Flask or specialized software - BentoML, KServe, etc)
"""
import pickle
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field, conint, confloat
from typing import Dict, Any, Literal

# request

Workclass = Literal[
    "State-gov",
    "Self-emp-not-inc",
    "Private",
    "Federal-gov",
    "Local-gov",
    "Self-emp-inc",
    "Without-pay",
]

Education = Literal[
    "Bachelors",
    "HS-grad",
    "11th",
    "Masters",
    "9th",
    "Some-college",
    "Assoc-acdm",
    "7th-8th",
    "Doctorate",
    "Assoc-voc",
    "Prof-school",
    "5th-6th",
    "10th",
    "Preschool",
    "12th",
    "1st-4th",
]

MaritalStatus = Literal[
    "Never-married",
    "Married-civ-spouse",
    "Divorced",
    "Married-spouse-absent",
    "Separated",
    "Married-AF-spouse",
    "Widowed",
]

Occupation = Literal[
    "Adm-clerical",
    "Exec-managerial",
    "Handlers-cleaners",
    "Prof-specialty",
    "Other-service",
    "Sales",
    "Transport-moving",
    "Farming-fishing",
    "Machine-op-inspct",
    "Tech-support",
    "Craft-repair",
    "Protective-serv",
    "Armed-Forces",
    "Priv-house-serv",
]

Race = Literal[
    "White",
    "Black",
    "Asian-Pac-Islander",
    "Amer-Indian-Eskimo",
    "Other",
]

Sex = Literal["Male", "Female"]

NativeCountry = Literal[
    "United-States",
    "Cuba",
    "Jamaica",
    "India",
    "Mexico",
    "Puerto-Rico",
    "Honduras",
    "England",
    "Canada",
    "Germany",
    "Iran",
    "Philippines",
    "Poland",
    "Columbia",
    "Cambodia",
    "Thailand",
    "Ecuador",
    "Laos",
    "Taiwan",
    "Haiti",
    "Portugal",
    "Dominican-Republic",
    "El-Salvador",
    "France",
    "Guatemala",
    "Italy",
    "China",
    "South",
    "Japan",
    "Yugoslavia",
    "Peru",
    "Outlying-US(Guam-USVI-etc)",
    "Scotland",
    "Trinadad&Tobago",
    "Greece",
    "Nicaragua",
    "Vietnam",
    "Hong",
    "Ireland",
    "Hungary",
    "Holand-Netherlands",
]


class Adult(BaseModel):
	# numeric ranges from your describe() outputs
	age: (conint(ge=17, le=90))
	
	workclass: Workclass
	education: Education
	marital_status: MaritalStatus = Field(..., alias="marital-status")
	occupation: Occupation
	race: Race
	sex: Sex
	
	capital_gain: (conint(ge=0, le=99999)) = Field(..., alias="capital-gain")
	capital_loss: (conint(ge=0, le=4356)) = Field(..., alias="capital-loss")
	hours_per_week: (conint(ge=1, le=99)) = Field(..., alias="hours-per-week")
	
	native_country: NativeCountry = Field(..., alias="native-country")
	
	class Config:
		populate_by_name = True


# response
Probability = (confloat(ge=0.0, le=1.0))

class Prediction(BaseModel):
	income: bool
	probability: Probability

app = FastAPI(title='income-prediction')

with open('model.bin', 'rb') as f_in:
	pipeline = pickle.load(f_in)
	
def predict_single(adult):
	return float(pipeline.predict_proba(adult)[0, 1])
	
@app.post('/predict')
def predict(adult: Adult) -> Prediction:
	y_forest_pred = predict_single(adult.model_dump(by_alias=True))
	return Prediction(
		income = bool(y_forest_pred >= 0.5),
		probability = y_forest_pred
	)

if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=9696)
	