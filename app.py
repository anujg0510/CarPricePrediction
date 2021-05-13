from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('car_price_predictions.pkl', 'rb'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Age = 2021 - Year
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Kms_Driven2 = np.log(Kms_Driven)
        Seats = int(request.form['Seats'])

        FirstOwner = SecondOwner = ThirdOwner = FourthOwner = TestDriveCar = 0
        Owner = request.form['Owner']
        if(Owner == 'FirstOwner'):
            FirstOnwer = 1
        elif(Owner == 'SecondOwner'):
            SecondOwner = 1
        elif (Owner == 'ThirdOwner'):
            ThirdOwner = 1
        elif (Owner == 'FourthOwner'):
            FourthOwner = 1
        else:
            TestDriveCar = 1

        Fuel_Type_CNG = Fuel_Type_Diesel = Fuel_Type_Petrol = Fuel_Type_LPG = 0
        Fuel_Type = request.form['Fuel_Type']
        if(Fuel_Type == 'Petrol'):
            Fuel_Type_Petrol = 1
        elif(Fuel_Type == "Diesel"):
            Fuel_Type_Diesel = 1
        elif(Fuel_Type == "CNG"):
            Fuel_Type_CNG = 1
        else:
            Fuel_Type_LPG = 1

        Seller_Individual = Seller_Dealer = Seller_Trustmark = 0
        Seller_Type = request.form['Seller_Type']
        if(Seller_Type == 'Individual'):
            Seller_Individual = 1
        elif(Seller_Type == 'Dealer'):
            Seller_Dealer = 1
        else:
            Seller_Trustmark = 1

        Transmission_Manual = Transmission_Auto = 0
        Transmission = request.form['Transmission']
        if(Transmission == 'Mannual'):
            Transmission_Manual = 1
        else:
            Transmission_Auto = 1

        prediction = model.predict([[Kms_Driven2, Seats, Age, Fuel_Type_Diesel, Fuel_Type_LPG, Fuel_Type_Petrol,
                                     Seller_Individual, Seller_Trustmark, Transmission_Manual,
                                     FourthOwner, SecondOwner, TestDriveCar, ThirdOwner]])
        output = round(prediction[0],2)

        if output<0:
            return render_template('index.html', prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html', prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)