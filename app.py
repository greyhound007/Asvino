from flask import Flask,url_for
from google.cloud import bigquery
import os



#UPLOAD_FOLDER = os.path.join(PARENT_DIR, 'gene_data')
app = Flask(__name__)
app.secret_key = "secret key"
