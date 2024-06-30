# Apache Airflow 이미지 기반
FROM apache/airflow:2.9.2

# 작업 디렉토리 설정
WORKDIR /app/airflow

# requirements.txt 파일을 이미지로 복사
COPY requirements.txt .

# 필요한 Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# dags와 src 디렉토리를 이미지로 복사
COPY dags /app/airflow/dags
COPY src /app/airflow/dags/src