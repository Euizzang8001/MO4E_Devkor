from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def say_hello():
    print("Hello, Airflow!")

# DAG 정의
dag = DAG(
    'hello_airflow',
    schedule_interval=None,  # DAG 실행 일정을 설정하려면 이 부분을 수정하세요.
    start_date=datetime(2023, 10, 6),  # DAG 실행을 시작할 날짜를 설정하세요.
    catchup=False,  # 이전 실행을 캐치업할 것인지 여부를 설정하세요.
)

# "say_hello" 함수를 실행하는 PythonOperator를 정의합니다.
hello_task = PythonOperator(
    task_id='hello_task',
    python_callable=say_hello,
    dag=dag,
)

fxxx_task = PythonOperator(
    task_id='fxxx_task',
    python_callable=say_hello,
    dag=dag,
)
# DAG 실행 순서를 정의합니다.
hello_task >> fxxx_task