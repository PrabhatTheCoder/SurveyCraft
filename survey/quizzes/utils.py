import pandas as pd
import os
from celery import shared_task
from users.models import AppUsers
from company.models import App
from quizzes.models import Audience

@shared_task
def ingest_data_task(file_path,audience_id, app_id):
    ingest_customer_data(file_path, audience_id, app_id)
    os.remove(file_path)     



def ingest_customer_data(file_path, audience_id, app_id):
    print(f"Ingesting customer data from {file_path}")
    data = pd.read_excel(file_path)
    print(f"Data read successfully: {data.head()}")
    
    app_instance = App.objects.get(id=app_id)
    audience_instance = Audience.objects.get(id=audience_id)
    for _, row in data.iterrows():  
        if isinstance(row, pd.Series): 
            extra_details = {
                key: str(row[key])
                for key in data.columns
                if key not in ['enrollment_no', 'Name', 'app_id', 'audience']
            }
            
            AppUsers.objects.update_or_create(
                id=row['enrollment_no'], 
                defaults={
                    'name': row['Name'],
                    'audience': audience_instance,
                    'app': app_instance,
                    'extra_details': extra_details, 
                },
            )
        else:
            print(f"Skipping row with invalid structure: {row}")

