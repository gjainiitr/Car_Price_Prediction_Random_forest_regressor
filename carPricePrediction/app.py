from flask import Flask, request, render_template
import pickle
import numpy as np
import pandas as pd
app = Flask(__name__)

model = pickle.load(open('random_forest_regression_model.pkl','rb'))

@app.route('/')
def hello_world():
    return render_template('./home.html')

# How to normalize data after importing in flask? Here, we are not normalizing as Random forest does not need it
@app.route('/predict', methods=['POST','GET'])
def predict():
    #define logic for temp    
    Present_Price = int(request.form["curr_price"])
    Kms_Driven = int(request.form["kms_driven"])
    Owner = int(request.form["owner-type"])
    age = 2020-int(request.form["year"])
    fuel = int(request.form["fuel-type"])
    if fuel == -1:
        Fuel_Type_Diesel = 0
        Fuel_Type_Petrol = 0
    elif fuel == 0:
        Fuel_Type_Diesel = 0
        Fuel_Type_Petrol = 1
    else:
        Fuel_Type_Diesel = 1
        Fuel_Type_Petrol = 0

    seller = int(request.form["seller-type"])
    if seller == 1:
        Seller_Type_Individual = 1
    else:
        Seller_Type_Individual = 0
    transmission = int(request.form["transmission"])
    if transmission == 1:
        Transmission_Manual = 1
    else:
        Transmission_Manual = 0
    
    """
    data = {
        'Present_Price':[int(request.form["curr_price"])],
        'Kms_Driven':[int(request.form["kms_driven"])],
        'Owner':[int(request.form["owner-type"])],
        'age':[2020-int(request.form["year"])],
        'Fuel_Type_Diesel':[(int(request.form["fuel-type"]) ==1)],
        'Fuel_Type_Petrol':[(int(request.form["fuel-type"]) ==0)],
        'Seller_Type_Individual':[(int(request.form["seller-type"]) ==1)],
        'Transmission_Manual':[(int(request.form["transmission"]) ==1)]}
    data = {'Present_Price':[45.35],'Kms_Driven':[4568],'Owner':[2],'age':[7],
        'Fuel_Type_Diesel':[0],
        'Fuel_Type_Petrol':[1],
        'Seller_Type_Individual':[0],
        'Transmission_Manual':[1]}
    """


    
    output = model.predict([[ Present_Price, Kms_Driven,Owner,age,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual, Transmission_Manual ]])
    output = round(output[0], 2)
    #output = np.fromstring(ts, dtype=int)
    #return output
    return render_template('result.html',pred="You can sell this car for {:.2f} lakhs".format(output))

if __name__ == "__main__":
    app.run(debug=True)