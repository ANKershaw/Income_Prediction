import requests
adults = [
	{
	  "age": 23,
	  "workclass": "Private",
	  "education": "Some-college",
	  "marital-status": "Never-married",
	  "occupation": "Handlers-cleaners",
	  "race": "White",
	  "sex": "Female",
	  "capital-gain": 0,
	  "capital-loss": 0,
	  "hours-per-week": 18,
	  "native-country": "United-States"
	},
	{
	  "age": 54,
	  "workclass": "State-gov",
	  "education": "HS-grad",
	  "marital-status": "Separated",
	  "occupation": "Adm-clerical",
	  "race": "Black",
	  "sex": "Female",
	  "capital-gain": 3887,
	  "capital-loss": 0,
	  "hours-per-week": 35,
	  "native-country": "United-States"
	},
	{
	  "age": 23,
	  "workclass": "Private",
	  "education": "Some-college",
	  "marital-status": "Never-married",
	  "occupation": "Other-service",
	  "race": "White",
	  "sex": "Female",
	  "capital-gain": 0,
	  "capital-loss": 0,
	  "hours-per-week": 40,
	  "native-country": "United-States"
	},
	{
	  "age": 34,
	  "workclass": "Private",
	  "education": "HS-grad",
	  "marital-status": "Married-civ-spouse",
	  "occupation": "Craft-repair",
	  "race": "White",
	  "sex": "Male",
	  "capital-gain": 0,
	  "capital-loss": 0,
	  "hours-per-week": 30,
	  "native-country": "Germany"
	},
	{
	  "age": 37,
	  "workclass": "Private",
	  "education": "Some-college",
	  "marital-status": "Married-civ-spouse",
	  "occupation": "Exec-managerial",
	  "race": "Asian-Pac-Islander",
	  "sex": "Male",
	  "capital-gain": 0,
	  "capital-loss": 0,
	  "hours-per-week": 55,
	  "native-country": "United-States"
	}
	]

answers = [0.002607,0.018577,0.004460,0.202992,0.550278,0.119872,0.486905,0.317298,0.800876,0.237507]
#url = 'http://127.0.0.1:9696/predict',
url = 'https://damp-field-1507.fly.dev/predict'
for i, adult in enumerate(adults):
	response = requests.post(url=url, json=adult)
	print(response.json())
	result = response.json()
	print(f"predicted that the status [income <= 50k] is {result['income']} for this adult. "
	      f"{round(result['probability']*100,2)}% probability. Expected answer: {round(answers[i]*100.0,2)}%\n")
		