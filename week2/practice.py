from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import numpy as np
import torch
from torch import nn, optim
from pykrx import stock

ohlcv = []

idx = 0
split_index = 0

train_idx = []
val_idx = []
x_train, y_train = [], []#trainset과 trainset의 label생성
x_val, y_val = [], []

#create tensor at CPU #tensor는 3차원 이상의 자료구조(매트릭스 이상의)
x_train_tensor = torch.as_tensor(x_train)
y_train_tensor = torch.as_tensor(y_train)

    #create tensor at GPU
device = 'cuda' if torch.cuda.is_available() else 'cpu'
x_train_tensor = torch.as_tensor(x_train).to(device)
y_train_tensor = torch.as_tensor(y_train).to(device)

def say_hello():
    ohlcv = stock.get_market_ohlcv("20140101", "20230921", "035720")
    N = len(ohlcv['시가'])
    idx = np.arange(N)
    split_index = int(N * 0.8)
    
    train_idx = idx[:split_index]
    val_idx = idx[split_index:]

    # 날짜를 x로, ohlcv['시가']를 y로 설정합니다.
    x = ohlcv.index  # 날짜 정보를 x로 사용합니다.
    y = ohlcv['시가']

    # trainset과 trainset의 label을 생성합니다.
    x_train, y_train = x[train_idx], y[train_idx]
    print("Train X:", x_train)
    print("Train Y:", y_train)

    # validation set과 validation set의 label을 생성합니다.
    x_val, y_val = x[val_idx], y[val_idx]
    print("Validation X:", x_val)
    print("Validation Y:", y_val)
    
def say_bye():
    lr=0.1
    epochs=1000
    #create tensor at CPU #tensor는 3차원 이상의 자료구조(매트릭스 이상의)
    x_train_tensor = torch.as_tensor(x_train)
    y_train_tensor = torch.as_tensor(y_train)

        #create tensor at GPU
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    x_train_tensor = torch.as_tensor(x_train).to(device)
    y_train_tensor = torch.as_tensor(y_train).to(device)

    b = torch.randn(1, requires_grad=True, dtype=torch.float, device=device) #requires_grad means this param is
    w = torch.randn(1, requires_grad=True, dtype=torch.float, device=device)

    parameters = [b, w]
    optimizer = optim.SGD(parameters, lr = lr)
    mse_loss = nn.MSELoss() 
    for epoch in range(epochs):
        #Loss computation
        y_hat = b + w * x_train_tensor
        loss = mse_loss(y_hat, y_train_tensor)

        #gradient computation and descent
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    print(w, b)

# DAG 정의
dag = DAG(
    'why_the_first.py_dont_run',
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
    python_callable=say_bye,
    dag=dag,
)
# DAG 실행 순서를 정의합니다.
hello_task >> fxxx_task