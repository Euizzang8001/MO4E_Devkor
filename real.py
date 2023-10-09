#example_branch_python_operator_decorator


from __future__ import annotations  

import pendulum

from airflow import DAG
from airflow.operators.python import PythonOperator
import torch
from pykrx import stock
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
import numpy as np

scaler2 = MinMaxScaler()
scaler3 = MinMaxScaler()
scale_cols_for_X = ['시가', '고가', '저가', '거래량']
scale_cols_for_y = ['종가']
ohlcv = []
X = []
y = []
result_model = tf.keras.Model()
x_train, x_valid, y_train, y_valid = []

with DAG(
    dag_id="first_stock_AI",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    schedule="@daily",
    tags=["torch", "pykrx", "numpy"],
) as dag:
    def data_set():
        global ohlcv, X, y
        ohlcv = stock.get_market_ohlcv("20140101", "20230921", "035720")
        ohlcv.index = pd.to_datetime(ohlcv.index)
        tests = scaler2.fit_transform(ohlcv[scale_cols_for_X])
        tests2 = scaler3.fit_transform(ohlcv[scale_cols_for_y])
        X = np.array([tests[i:i+1] for i in range(tests.shape[0]-1)])
        y = np.array([tests2[i+1] for i in range(tests2.shape[0]-1)])

    def data_for_test():
        global x_train, x_valid, y_train, y_valid
        x_train, x_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2)

    def forcompileandtrain():
        global result_model
        result_model.compile(optimizer='adam', loss='mean_squared_error', metrics=['acc'])
        early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)
        result_model.fit(x_train, y_train, batch_size=1, epochs=100, validation_data=(x_valid, y_valid), callbacks=[early_stop])

    def result():
        a = scaler2.transform([[45100, 45650, 44800, 1395423]])
        print(a)
        test = result_model.predict(np.array([a]))
        print(scaler3.inverse_transform(test))

    data_get = PythonOperator(
        task_id = "first",
        python_callable = data_set,
    )
    data_transform = PythonOperator(
        task_id = 'second',
        python_callable = data_for_test,
    )
    data_compile_and_test = PythonOperator(
        task_id = 'third',
        python_callable = forcompileandtrain,
    )
    data_result = PythonOperator(
        task_id = 'forth',
        python_callable = result(),
    )
    data_get >> data_transform
    data_transform >> data_compile_and_test
    data_compile_and_test >> data_result