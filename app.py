from flask import Flask,url_for
from google.cloud import bigquery
import os




app = Flask(__name__)
app.secret_key = "secret key"
client = bigquery.Client()
dataset_id = "{}.risk_analysis".format(client.project)
