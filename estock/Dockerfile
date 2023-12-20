FROM apache/airflow:2.5.3

COPY requirements.txt /

RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt

# 
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]