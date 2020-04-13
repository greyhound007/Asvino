import os

from app import app
#,dataset_id,client
from flask import Flask, flash, request, redirect, render_template,session
from werkzeug.utils import secure_filename
#import csv,pandas
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

            if request.form.get("gene_test")=="no":
                g="no"
            
            else:
                g=request.form.get("gene_type")
            
            factors = OrderedDict([
                ('family_history', request.form["family_history"]), #1
                ('sex',request.form["Sex"]), #1
                ('menarche_age' ,  request.form.get("menarche_age")), #3
                ('children',request.form.get("children")), #1
                ('age_of_first_birth',  request.form.get("age_of_first_birth")),#2
                ('oral_contraception',  request.form.get("oral_contraception")),#2
                ('mht', request.form.get("mht")),#menopause hormone replacement 0
                ('bmi',  request.form.get("bmi")) ,#body mass index 1
                ('alcohol',  request.form.get("alcohol")), #alcohol intake in grams/day 3
                ('age_of_menopause',request.form.get("age_of_menopause")), #0
                ('height',request.form.get("height")),#in cms 2
                ('gene_type',g)
                 ])

            
            session['factor']=factors
            
            score = breast_factor_score(factors)

            #Save snp file
            # check if the post request has the file part

            #
            '''
            if 'file'  in request.files:
                
                file = request.files['file']
                
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #change filename to id of user
                    print(filename)
                    
                    session['files']=filename
                    files=filename
                            
                    filename=session['files']
                    print(filename)    
            
                
                    #Convert file to csv in order to upload to big query
                    f= os.path.join(app.config['UPLOAD_FOLDER'], file_header(filename)+'.csv')
                    if filename.rsplit('.', 1)[1].lower() != "csv":
                        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as in_file:

                            stripped = (line.strip() for line in in_file)
                            lines = (line.split("\t")[0]+"\n" for line in stripped if line and line[0]!='#')
                            print(f)
                            with open(f, 'w') as out_file:
                                out_file.write("rsid\n")
                                for line in lines:
                                    out_file.write(line)
                                
                    #generate testid     
                    #Update test table with info


                    #Create table for user and load into bigquery
                    # table_id = "your-project.your_dataset.your_table_name"
                    table_id= "{}.{}".format(dataset_id,file_header(filename))  #change to testid
                        
                    schema = [
                            bigquery.SchemaField("rsid", "STRING", mode="REQUIRED"),
                        

                        ]
                    try: 
                        table = bigquery.Table(table_id, schema=schema)
                        table = client.create_table(table)  # Make an API request.
                        print(
                                "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
                                )
                    
                        
                        table_ref = table_id       
                        job_config = bigquery.LoadJobConfig()
                        job_config.source_format = bigquery.SourceFormat.CSV
                        job_config.skip_leading_rows = 1
                            

                        with open(f, "rb") as source_file:
                            job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

                        job.result()  # Waits for table load to complete.

                        print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))

                        query = """
                                    SELECT disease,COUNT(*)
                                    FROM `{}` as u , `{}.snpedia` as s 
                                        WHERE s.rsid = u.rsid
                                        GROUP BY disease
                                        
                                    """.format(table_id,dataset_id)
                        query_job = client.query(query) 
                        print("The query data:")
                        for row in query_job:
                        # Row values can be accessed by field name or index.
                            print("disease={}, count={}".format(row[0], row[1]))
                        breast_gene_count = row[1]    
                        score = score + breast_gene_count    
                    except:
                        return render_template('upload.html',message="Invalid file")

                    
                else:
                    
                    return render_template("upload.html", message="Allowed file type is .txt or .csv")
                
            else:
                files="na"
                session['files']="na"
                
            '''
            #              


                
            return render_template('risk_analysis.html',score=score)
    else:

        return render_template('upload.html') #pass user

# 
'''@app.route('/review', methods=['POST','GET'])    #dashboard/id
def review():
    score =0
    breast_gene_count=0
    factors=session['factor']
    
    if request.method == 'POST':
       

        return render_template('risk_analysis.html',score=score)
    else:
        return render_template('review.html',factors=session['factor'])

'''#
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
