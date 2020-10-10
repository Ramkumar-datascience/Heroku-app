import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
from sklearn.metrics import accuracy_score,precision_score
import csv
import time


app = Flask(__name__)
model = pickle.load(open('rf_model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('data.html')

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
	if request.method == 'POST':
		print('HIII')
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
		print('name is :',row)
		with open('names_list.csv' , 'a') as f:
			write = csv.writer(f) 
			#write.writerow(col) 
			write.writerows(row)
		
		return render_template('data.html', data=acc , data2=pre)

if __name__ == "__main__":
    app.run(debug=True)
