from flask import Flask,url_for
from google.cloud import bigquery
import os




app = Flask(__name__)
app.secret_key = "secret key"
client = bigquery.Client.from_service_account_json("C:\Users/rayel\Downloads\secure-potion-270613-c923fa84a6fc.json")
dataset_id = "{}.risk_analysis".format(client.project)
