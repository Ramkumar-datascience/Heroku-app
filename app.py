import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
from sklearn.metrics import accuracy_score,precision_score


app = Flask(__name__)
model = pickle.load(open('rf_model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
	input_data = pd.read_csv('test.csv')
	b = []
	for i in input_data['Class']:
		#print(i)
		b.append(i)
	if request.method == 'POST':
		print('HIII')
		file = request.form['csv_file']
		data = pd.read_csv(file)
		data1=[]
		for row in data.iloc[:,-1]:
			data1.append(row)
		int_features = [x for x in data1]
		print(int_features)
		#final_features = [np.array(int_features)]
		#prediction = model.predict([int_features])
		#print(y_test)
		return render_template('index.html', data=accuracy_score(b,int_features))

if __name__ == "__main__":
    app.run(debug=True)