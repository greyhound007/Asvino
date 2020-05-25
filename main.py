import os

from app import app,dataset_id,client
from flask import Flask, flash, request, redirect, render_template,session
from werkzeug.utils import secure_filename
from google.cloud import bigquery
from collections import OrderedDict 
from factor import breast_factor_score
import uuid

ALLOWED_EXTENSIONS = set(['txt'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def file_header(filename):
	return '.' in filename and filename.rsplit('.', 1)[0].lower()
	
filestatus=False

@app.route('/', methods=['POST','GET'])   
def home():

    return render_template('home.html')
@app.route('/test', methods=['POST','GET'])   
def fill_form():

    
    
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

            
           
            
            score = breast_factor_score(factors)
            if score < 5 :
                risk="low"
            elif score >5 and score <=20 : 
                risk="medium"
            else:
                risk="high"
            idd=str(uuid.uuid4())
            query = """
                                            insert into
                                                 `{}.form` 
                                                    values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','','')
                                                    
                                                    
                                                """.format(dataset_id,request.form["family_history"],age, request.form.get("menarche_age"),request.form.get("age_of_first_birth"), request.form.get("mht"),request.form.get("alcohol"),request.form.get("age_of_menopause"),request.form.get("height"),g,request.form.get("radiation_exposure"),risk,idd, request.form["fears"])
            query_job = client.query(query) 
            session['id']=idd
            


                
            return render_template('risk_analysis.html',score=score)
    else:

        return render_template('test.html') 


@app.route('/feedback', methods=['POST','GET'])    
def feedback():
    if request.method == 'POST':
        idd = session['id']
        rating=""
        feedback=""
        rating=request.form["emotion"]
        feedback=request.form.get("fb")
        
        
        try: 
                            query = """
                                        update 
                                            `{}.form` as t
                                        set t.rating = '{}',t.feedback='{}' 
                                        where  t.id = '{}'
                            
                            """.format(dataset_id,rating,feedback,idd)
                            query_job = client.query(query) 

        except:
                print("Unable to update form data of {}".format(idd) )
        
        return redirect("/final")

@app.route('/final', methods=['POST','GET'])    
def final():
    session.pop("idd",None)
    return render_template("final.html")

if __name__ == "__main__":
    app.run(debug=True)
