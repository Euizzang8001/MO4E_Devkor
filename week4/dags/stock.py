import pendulum
from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.stock_algo import get_today, get_nexon, nexon_xy, nexon_prep, lstm_nexon, predict_or_check


# from src.stock_algo import

kst = pendulum.timezone('Asia/Seoul')
dag_name = "Euizzang_First_Dag"

default_args = {
    'owner': 'Euizzang',
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}
with DAG(
    dag_id=dag_name,
    default_args=default_args,
    description='어려우어어어어어어어어',
    schedule_interval=timedelta(minutes=10),
    start_date = pendulum.datetime(2023, 11, 6, tz=kst),
    catchup=False,
    tags=['stock', 'Euizzang']
) as dag:
    get_nexon_task = PythonOperator(
        task_id='get_nexon_task',
        python_callable=get_nexon,
    )
    nexon_xy_task = PythonOperator(
        task_id = 'nexon_xy_task',
        python_callable=nexon_xy,
    )
    nexon_prep_task = PythonOperator(
        task_id='nexon_prep_task',
        python_callable=nexon_prep,
    )
    lstm_nexon_task = PythonOperator(
        task_id='lstm_nexon_task',
        python_callable= lstm_nexon,
    )
    predict_or_check_task = PythonOperator(
        task_id = 'predict_or_check_task',
        python_callable=predict_or_check,
    )
    get_nexon_task >> nexon_xy_task >> nexon_prep_task >> lstm_nexon_task >> predict_or_check_task