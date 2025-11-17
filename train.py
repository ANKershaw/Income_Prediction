"""
This script will include:
	Training the final model
	Saving it to a file (e.g. pickle) or saving it with specialized software (BentoML)
"""
import pickle

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline


def load_data():
	column_names = ['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation',
	                'relationship', 'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income']
	data = pd.read_csv('./Data/adult/adult.data', sep=',', names=column_names)
	print('data loaded')
	return data
	
	
def clean_data(data):
	# the fnlwgt represents a weighting factor, and it will be discarded for simplicity
	data.drop('fnlwgt', axis=1, inplace=True)
	
	# the education and education-num columns are redundant so we will remove education-num
	data.drop('education-num', axis=1, inplace=True)
	
	# the marital-status and relationship columns are redundant so we will remove relationship
	data.drop('relationship', axis=1, inplace=True)
	
	categorical = ['workclass', 'education', 'marital-status', 'occupation', 'race', 'sex', 'native-country', 'income']
	
	# addressing missing/placeholder values
	# removing the rows that have ' ?' for values
	data = data[data['workclass'] != ' ?']
	data = data[data['native-country'] != ' ?']
	data = data[data['occupation'] != ' ?']
	
	# removing the leading and trailing whitespace from categorical variables
	data[categorical] = data[categorical].apply(lambda x: x.str.strip())
	data['education'].unique()
	
	# changing the income value from text to numerical
	data['income'] = data['income'].map({'<=50K': 0, '>50K': 1})
	print('data cleaned')
	return data

def train_model(data):
	# split up the dataset
	df_full_train, df_test = train_test_split(data, test_size=0.2, random_state=42)
	df_train, df_val = train_test_split(df_full_train, test_size=0.25, random_state=42)
	
	df_train = df_train.reset_index(drop=True)
	df_val = df_val.reset_index(drop=True)
	df_test = df_test.reset_index(drop=True)
	
	y_train = df_train.income.values
	y_val = df_val.income.values
	y_test = df_test.income.values
	
	del df_train['income']
	del df_val['income']
	del df_test['income']
	
	# one-hot encoding
	dv = DictVectorizer(sparse=False)
	X_train = dv.fit_transform(df_train.to_dict('records'))
	X_val = dv.transform(df_val.to_dict('records'))
	
	rf = RandomForestClassifier(n_estimators=300, max_depth=15, min_samples_leaf=1, random_state=1)
	rf.fit(X_train, y_train)
	y_forest_pred = rf.predict_proba(X_val)[:,1]
	forest_auc = roc_auc_score(y_val, y_forest_pred)
	
	# create pipeline
	pipeline = make_pipeline(DictVectorizer(), RandomForestClassifier(n_estimators=300, max_depth=15,
	                                                            min_samples_leaf=1, random_state=1))
	train_dict = df_train.to_dict('records')
	pipeline.fit(train_dict, y_train)
	
	print('pipeline created')
	return pipeline, forest_auc, df_val.to_dict('records'), y_val
	
def save_model(filename, pipeline):
	with open('model.bin', 'wb') as f_out:
		pickle.dump(pipeline, f_out)
	print(f'model saved to {filename}')
	
def check_model(pipeline, test_auc, val_df, y_val):
	print(f'auc before export: {test_auc}')
	y_forest_pred = pipeline.predict_proba(val_df)[:,1]
	forest_auc = roc_auc_score(y_val, y_forest_pred)
	print(f'auc after export: {forest_auc}')
	if test_auc == forest_auc:
		print(f'auc values match.')
	else:
		print(f'auc values do not match. double check the code.')

	
	
df = load_data()
df = clean_data(df)
pipeline, test_auc, X_val, y_val = train_model(df)
save_model('model.bin', pipeline)
check_model(pipeline, test_auc, X_val, y_val)