#!/usr/bin/python3

import pandas as pd
from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np

#from sklearn import preprocessing, metrics


app = Flask(__name__)


model = pickle.load(open('decision_tree_model.pkl', 'rb'))
@app.route('/')
def Home():
	#return 'Hello Pranav'
	return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
	Fuel_Type_Diesel=0
	if request.method == 'POST':
		
		test_data=[]
		Present_Price=float(request.form['Present_Price'])
		test_data.append(Present_Price)
		Kms_Driven=int(request.form['Kms_Driven'])
		test_data.append(Kms_Driven)
		Owner=int(request.form['Owner'])
		test_data.append(Owner)

		Year = int(request.form['Year'])
		age=2020-Year
		test_data.append(age)
		
		
		Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
		if(Fuel_Type_Petrol=='Petrol'):
			Fuel_Type_Petrol=1
			Fuel_Type_Diesel=0
		elif(Fuel_Type_Petrol=='Diesel'):
			Fuel_Type_Petrol=0
			Fuel_Type_Diesel=1
		else:
			Fuel_Type_Petrol=0
			Fuel_Type_Diesel=0

		test_data.append(Fuel_Type_Diesel)
		test_data.append(Fuel_Type_Petrol)
			

		Seller_Type_Individual=request.form['Seller_Type_Individual']
		if(Seller_Type_Individual=='Individual'):
			Seller_Type_Individual=1
		else:
			Seller_Type_Individual=0

		test_data.append(Seller_Type_Individual)
		Transmission_Mannual=request.form['Transmission_Mannual']
		if(Transmission_Mannual=='Mannual'):
			Transmission_Mannual=1
		else:
			Transmission_Mannual=0
		test_data.append(Transmission_Mannual)
		print("INPUT DATA",test_data)
		prediction=model.predict([test_data])
		print("PREDICTED ANSWER",prediction)
		output=round(prediction[0],2)
		if output<0:
			return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
		else:
			return render_template('index.html',prediction_text="You Can Sell The Car at {} lac".format(output))
	else:
		return render_template('index.html')


if __name__ == '__main__':
	app.run()
