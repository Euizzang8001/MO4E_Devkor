FROM apache/airflow:2.5.3 
ADD requirements.txt . 
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt


FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app

COPY ./ /app

# FastAPI를 Uvicorn과 함께 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]