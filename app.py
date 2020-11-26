import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
from sklearn.metrics import accuracy_score,precision_score
import csv
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials


app = Flask(__name__)
model = pickle.load(open('rf_model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('sample.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
	input_data = pd.read_csv('test.csv')
	b = ['Benign', 'Benign', 'Benign', 'malignant', 'Benign', 'Benign',
       'malignant', 'malignant', 'Benign', 'Benign', 'malignant',
       'Benign', 'Benign', 'malignant', 'Benign', 'Benign', 'malignant',
       'Benign', 'Benign', 'Benign', 'Benign', 'Benign', 'Benign',
       'malignant', 'Benign', 'Benign', 'Benign', 'Benign', 'Benign',
       'malignant', 'malignant', 'malignant', 'malignant', 'Benign',
       'Benign', 'malignant', 'Benign', 'Benign', 'Benign', 'malignant',
       'Benign', 'malignant', 'Benign', 'malignant', 'Benign', 'Benign',
       'Benign', 'Benign', 'Benign', 'Benign', 'Benign', 'malignant',
       'malignant', 'Benign', 'malignant', 'malignant', 'malignant',
       'Benign', 'malignant', 'Benign', 'Benign', 'Benign', 'Benign',
       'Benign', 'malignant', 'malignant', 'Benign', 'Benign', 'Benign',
       'malignant', 'malignant', 'malignant', 'malignant', 'malignant',
       'malignant', 'Benign', 'malignant', 'Benign', 'Benign', 'Benign',
       'Benign', 'Benign', 'Benign', 'malignant', 'malignant', 'Benign',
       'Benign', 'Benign', 'malignant', 'malignant', 'Benign', 'Benign',
       'malignant', 'Benign', 'Benign', 'Benign', 'Benign', 'malignant',
       'Benign', 'Benign', 'Benign', 'Benign', 'Benign', 'Benign',
       'malignant', 'Benign', 'malignant', 'malignant', 'malignant',
       'Benign', 'Benign', 'Benign', 'Benign', 'Benign', 'malignant',
       'malignant', 'Benign', 'Benign', 'Benign', 'Benign', 'Benign',
       'malignant', 'malignant', 'malignant', 'malignant', 'Benign',
       'Benign', 'malignant', 'Benign', 'Benign', 'Benign', 'Benign',
       'Benign', 'malignant', 'Benign', 'malignant', 'malignant',
       'malignant', 'Benign', 'Benign', 'Benign', 'Benign', 'Benign',
       'Benign', 'Benign', 'malignant', 'Benign', 'Benign', 'Benign',
       'malignant', 'Benign', 'Benign', 'malignant', 'Benign', 'Benign',
       'Benign', 'Benign', 'Benign', 'Benign', 'Benign', 'Benign',
       'malignant', 'malignant', 'malignant', 'Benign', 'malignant',
       'Benign', 'Benign', 'Benign', 'malignant', 'Benign']
	#for i in input_data['Class']:
		#print(i)
		#b.append(i)
		# https://www.youtube.com/watch?v=cnPlKLEGR7E (for Google sheet linking)
	if request.method == 'POST':
		scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

		creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

		client = gspread.authorize(creds)
		sheet = client.open("Hackathon-results").sheet1
		
		file = request.form['csv_file']
		data = pd.read_csv(file)
		data1=[]
		for row in data.iloc[:,-1]:
			data1.append(row)
		int_features = [x for x in data1]
		#print(int_features)
		#final_features = [np.array(int_features)]
		#prediction = model.predict([int_features])
		#print(y_test)
		
		col = ['Name', 'Batch No', 'file']
		name = [x for x in request.form.values()]
		acc = accuracy_score(b,int_features)
		pre = precision_score(b,int_features,average='macro')
		
		named_tuple = time.localtime() # get struct_time
		dates = time.strftime("%m/%d/%Y", named_tuple)
		times = time.strftime(" %H:%M:%S", named_tuple)
		
		row = [ name + [str(acc)] + [str(pre)] + [str(dates)] + [str(times)]]
		sheet.insert_rows(row)
		
		return render_template('sample.html', data=acc , data2=pre)

if __name__ == "__main__":
    app.run(debug=True)
