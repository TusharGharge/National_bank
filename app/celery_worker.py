from fastapi import FastAPI, HTTPException, BackgroundTasks
from celery import Celery
import redis
import json
from datetime import datetime

celery = Celery(
    'celery_worker',
    broker='redis://localhost:6379/0',  # Redis broker
    backend='redis://localhost:6379/0'  # Redis backend
)
# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# @celery.task
# def generate_monthly_statements():
#     # Logic to generate monthly statements
#     # For demo, let's just print the current month and year
#     current_month_year = datetime.now().strftime("%B %Y")
#     print("Generating monthly statements for:", current_month_year)
