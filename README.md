# Income Prediction

# Description of the problem
The goal of this project is a simple one: when provided with data such as occupation, country, and age, can we predict income? Specifically, can we predict if a person's income will be over \$50k or not?

The uses for this kind of data are endless, but here are a few:
* Marketing - target the higher or lower income group, whatever matches your brand needs
* Finance - use as a factor to determine lending terms or detect fraud
* Politics - use to help decide where you should be focusing campaign efforts
* Outreach - determine underserved areas and provide assistance
* Housing - locate areas where affordable housing should be built 
<br></br>

# Instructions on how to run the project

## Get the code
In your terminal:
1. Download repo: `git clone https://github.com/ANKershaw/Income_Prediction.git` 
2. Navigate to project folder:`cd Income_Prediction`. All future commands assume you're in this folder.
<br></br>
## Dependency Management
1. Install uv, following the [instructions here](https://docs.astral.sh/uv/getting-started/installation/)
2. Install packages: `uv sync --locked`
<br></br>
## If you want to test the deployed service
I've provided a script to do this. You can run it via: <br>
`uv run income_prediction.py .`<br>
<br>
The service is currently deployed here: https://damp-field-1507.fly.dev/predict <br>
The swagger page is here: https://damp-field-1507.fly.dev/docs <br>
The service will stay running until January 1, 2026, unless fly.io becomes prohibitively expensive. 

## If you want to deploy the docker container locally
1. Build the container `docker build -t income-prediction`
2. Run the service `docker run -it --rm -p 9696:9696 income-prediction`
<br></br>
### How to test a local deploy 
#### Browser
In your browser, navigate to http://0.0.0.0:9696/docs and use the swagger interface with this data: <br>
```
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
}
```
#### via Curl
here is the curl command:
```
curl -X 'POST' \
  'http://0.0.0.0:9696/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "age": 17,
  "workclass": "State-gov",
  "education": "Bachelors",
  "marital-status": "Never-married",
  "occupation": "Adm-clerical",
  "race": "White",
  "sex": "Male",
  "capital-gain": 99999,
  "capital-loss": 4356,
  "hours-per-week": 1,
  "native-country": "United-States"
}'
```

## Data Source
The dataset is from the UC Irvine Machine Learning Repository. The link is here: https://archive.ics.uci.edu/dataset/2/adult.
The data is pulled from the 1994 Census database. With inflation, the \$50,000 benchmark is around \$111,000 today. 

## Context for this Project
This repo is the midterm project for DataTalks Club's Machine Learning Zoomcamp. This repo is based around the specifications and requirements listed here: https://github.com/DataTalksClub/machine-learning-zoomcamp/tree/master/projects.
