import pendulum
from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.stock_algo import finish, revise, get_today, get_stock, stock_xy, predict_or_check, revise


# from src.stock_algo import

kst = pendulum.timezone('Asia/Seoul')
dag_name = "STOCK_ED_U"

default_args = {
    'owner': 'Euizzang',
    'retries': 3,
    'retry_delay': timedelta(minutes=1) 
}
with DAG(
    dag_id=dag_name,
    default_args=default_args,
    description='stock',
    schedule_interval=timedelta(hours=24),
    start_date = pendulum.datetime(2023, 12, 3, 16, 0, 0, tz=kst),
    catchup=False,
    tags=['stock', 'Euizzang']

) as dag:
    get_samsung_task = PythonOperator(
        task_id='get_samsung_task',
        python_callable=get_stock,
    )
    samsung_xy_task = PythonOperator(
        task_id = 'samsung_xy_task',
        python_callable=stock_xy,
    )
    predict_samsung_task = PythonOperator(
        task_id = 'predict_or_check_task',
        python_callable=predict_or_check,
    )
    
    finish_task = PythonOperator(
        task_id = 'finish_task',
        python_callable=finish,
    )
    revise_task = PythonOperator(
        task_id = 'revise_task',
        python_callable=revise,
    )
    get_samsung_task >> samsung_xy_task >> predict_samsung_task >> finish_task >> revise_task