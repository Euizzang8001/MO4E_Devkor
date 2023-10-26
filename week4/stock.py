import os
import pendulum
from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

# from src.stock_algo import

kst = pendulum.timezone('Asia/Seoul')
dag_name = os.path.basename(__file__).split('.')[0]

default_args = {
    'owner': 'Euizzang',
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}

# 계획
# 1. 주식을 받아옴
# 2. 어제와 비교했을 때 주가의 변동 여부 보여줌
# 3. 네이버의 주식을 받아옴
# 4. 네이버의 현재까지의 주가 분석(ml)
# 5. 
with DAG(
    dag_id=dag_name,
    default_args=default_args,
    description='어려우어어어어어어어어',
    schedule_dage = pendulum.datetime(2023, 10, 26, tz=kst),
    catchup=False,
    tags=['stock', 'Euizzang']
) as dag:
    #
    get_market_fundamental_task = PythonOperator(
        task_id = 'get_market_fundamental_task',
        python_callable=get_market_fundamental_task,
    )