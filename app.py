from flask import Flask,url_for
from google.cloud import bigquery
import os

# absolute path to this file
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
# absolute path to this file's root directory
PARENT_DIR = os.path.join(FILE_DIR, os.pardir) 

#UPLOAD_FOLDER = os.path.join(PARENT_DIR, 'gene_data')
app = Flask(__name__)
app.secret_key = "secret key"

#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
#client = bigquery.Client.from_service_account_json("C:\Users/rayel\Downloads\secure-potion-270613-c923fa84a6fc.json")
#dataset_id = "{}.risk_analysis".format(client.project)

