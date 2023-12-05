FROM apache/airflow:2.5.3 
ADD requirements.txt . 
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt

# 베이스 이미지 설정 (Python 3.8 기반의 공식 이미지 사용)
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# 컨테이너 실행 명령 설정 (uvicorn으로 FastAPI 앱 실행)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]