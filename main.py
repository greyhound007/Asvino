import os

from app import app
#,dataset_id,client
from flask import Flask, flash, request, redirect, render_template,session
from werkzeug.utils import secure_filename
import csv,pandas
from google.cloud import bigquery
from collections import OrderedDict 
from factor import breast_factor_score

ALLOWED_EXTENSIONS = set(['txt'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def file_header(filename):
	return '.' in filename and filename.rsplit('.', 1)[0].lower()
	
filestatus=False

#class User

@app.route('/', methods=['POST','GET'])    #dashboard/id
def fill_form():

    #get user info (query through id) 
    
    
    if request.method == 'POST':
            #OTHER FACTORS
            age=request.form["age"]
            if request.form.get("gene_test")=="no":
                g="no"
            
            elif (age == "-30" or age == "30-40") and (request.form.get("gene_type")=="40+") : 
                g="40-" 
            else:
                g=request.form.get("gene_type")
            
            factors = OrderedDict([
                ('family_history', request.form["family_history"]), #1
                ('age',age), #1
                ('menarche_age' ,  request.form.get("menarche_age")), #3
                ('age_of_first_birth',  request.form.get("age_of_first_birth")),#2
                ('mht', request.form.get("mht")),#menopause hormone replacement 0
                ('alcohol',  request.form.get("alcohol")), #alcohol intake in grams/day 3
                ('age_of_menopause',request.form.get("age_of_menopause")), #0
                ('height',request.form.get("height")),#in cms 2
                ('gene_type',g),
                ('radiation_exposure',request.form.get("radiation_exposure"))

                 ])

            
            session['factor']=factors
            
            score = breast_factor_score(factors)

            


                
            return render_template('risk_analysis.html',score=score)
    else:

        return render_template('upload.html') #pass user


@app.route('/risk_analysis', methods=['POST','GET'])    #dashboard/id
def risk():
    if request.method == 'POST':
        answer=request.form["gene_test"]
        message=""
        if answer == "yes":
            email= request.form.get("email")
            phone=request.form.get("phone")
            message="We will get back to you with the results shortly."
        return render_template("final.html",message=message)

if __name__ == "__main__":
    app.run(debug=True)
