#BIG QUERY SET UP. 


from google.cloud import bigquery
import app



dataset=bigquery.Dataset(app.dataset_id)
dataset.location="US"
dataset = app.client.create_dataset(dataset)  # Make an API request.
print("Created dataset {}.{}".format(app.client.project, dataset.dataset_id))


#snpedia table load
table_ref = "{}.snpedia".format(app.dataset_id)     
job_config = bigquery.LoadJobConfig()
job_config.source_format = bigquery.SourceFormat.CSV
job_config.skip_leading_rows = 1
                

with open("C:\Users/rayel\Downloads\snpedia.csv", "rb") as source_file:
                    job = app.client.load_table_from_file(source_file, table_ref, job_config=job_config)

job.result()  # Waits for table load to complete.

print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_ref))

