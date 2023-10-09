from pyexpat import features
from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd


app = Flask(__name__)
model = pickle.load(open("houseRent_gbr.pkl", "rb"))


@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")



@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        # features=[[x for x in request.form.values()]]

        BHK = int(request.form["BHK"])
        Size = int(request.form['Size'])

        area_type=request.form["Area Type"]
        if area_type == 'Built Area':
            Built_Area=1
            Super_Area=0
            Carpet_Area=0
        elif area_type == "Super Area":
            Built_Area=0
            Super_Area=1
            Carpet_Area=0
        elif area_type == "Carpet Area":
            Built_Area=0
            Super_Area=0
            Carpet_Area=1
        else:
            Built_Area=0
            Super_Area=0
            Carpet_Area=0


        # Area_Type=request.form['Area Type']
        # if (Area_Type=='Built Area'):
        #     Super_Area = 0
        #     Carpet_Area = 0
        #     Built_Area = 1
        # elif(Area_Type=='Carpet Area'):
        #     # Carpet Area=1
        #     Super_Area = 0
        #     Carpet_Area = 1
        #     Built_Area=0
        # elif(Area_Type=='Super Area'):
        #     Super_Area=1
        #     Carpet_Area=0
        #     Built_Area=0
        # else:
        #     Super_Area=0
        #     Carpet_Area=0
        #     Built_Area=0

        city = request.form['City']
        if (city=='Mumbai'):
            Mumbai=1
            Delhi=0
            Chennai=0
            Banglore=0
            Hyderabad=0
            Kolkata=0
        elif(city=='Delhi'):
            Mumbai=0
            Delhi=1
            Chennai=0
            Banglore=0
            Hyderabad=0
            Kolkata=0
        elif(city=='Chennai'):
            Mumbai=0
            Delhi=0
            Chennai=1
            Banglore=0
            Hyderabad=0
            Kolkata=0
        elif(city=='Banglore'):
            Mumbai=0
            Delhi=0
            Chennai=0
            Banglore=1
            Hyderabad=0
            Kolkata=0
        elif(city=='Hyderabad'):
            Mumbai=0
            Delhi=0
            Chennai=0
            Banglore=0
            Hyderabad=1
            Kolkata=0
        elif(city=='Kolkata'):
            Mumbai=0
            Delhi=0
            Chennai=0
            Banglore=0
            Hyderabad=0
            Kolkata=1
        else:
            Mumbai=0
            Delhi=0
            Chennai=0
            Banglore=0
            Hyderabad=0
            Kolkata=0

        furnishing_status=request.form['Furnishing Status']
        if (furnishing_status=='Semi-Furnished'):
            Semi_Furnished=1
            Unfurnished=0
            Furnished=0
        elif(furnishing_status=='Unfurnished'):
            Semi_Furnished=0
            Unfurnished=1
            Furnished=0
        elif(furnishing_status=='Furnished'):
            Semi_Furnished=0
            Unfurnished=0
            Furnished=1

        else:
            Semi_Furnished=0
            Unfurnished=0
            Furnished=0

        tenant_preferred=request.form['Tenant Preferred']
        if (tenant_preferred=='Bachelors/Family'):
            Bachelors_Family=1
            Bachelors=0
            Family=0
        elif(tenant_preferred=='Bachelors'):
            Bachelors_Family=0
            Bachelors=1
            Family=0
        elif(tenant_preferred=='Family'):
            Bachelors_Family=0
            Bachelors=0
            Family=1
        else:
            Bachelors_Family=0
            Bachelors=0
            Family=0

        max_floor=int(request.form['Max Floors'])

        floor_level=int(request.form['Floor Level'])

        Bathroom=int(request.form['Bathroom'])

        point_of_contact=request.form['Point of Contact']
        if (point_of_contact=='Contact Owner'):
            Contact_Owner=1
            Contact_Agent=0
            Contact_Builder=0
        elif(point_of_contact=='Contact Agent'):
            Contact_Owner=0
            Contact_Agent=1
            Contact_Builder=0
        elif(point_of_contact=='Contact Builder'):
            Contact_Owner=0
            Contact_Agent=0
            Contact_Builder=1
        else:
            Contact_Owner=0
            Contact_Agent=0
            Contact_Builder=0

        prediction=model.predict([[
            BHK,
            Size,
            Built_Area,
            Super_Area,
            Carpet_Area,
            Mumbai,
            Delhi,
            Chennai,
            Banglore,
            Hyderabad,
            Kolkata,
            Semi_Furnished,
            Unfurnished,
            Furnished,
            Bachelors_Family,
            Bachelors,
            Family,
            max_floor,
            floor_level,
            Bathroom,
            Contact_Owner,
            Contact_Agent,
            Contact_Builder,
        ]])

        output=round(prediction[0],2)


        return render_template('index.html',prediction_text="Your Apartment Rent price is Rs. {}".format(output))


    return render_template("index.html")
       

if __name__ == "__main__":
    app.run(debug=True)