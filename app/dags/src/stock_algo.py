import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pykrx import stock
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
import pendulum
import requests

back_url = "http://127.0.0.1:8000/estock"
dt_today = str(datetime.now().date())

def get_today():
    kst = pendulum.timezone('Asia/Seoul')
    current_time = datetime.now().astimezone(kst)
    dt_now = str(current_time.date())
    print(f'{dt_now} 기준')
    dt_now = ''.join(c for c in dt_now if c not in '-')
    return dt_now

def get_stock():
    dt_now = get_today()
    ticker_stock = stock.get_market_ohlcv("20150925", dt_now, '005930')
    ticker_stock.to_csv(f'./{dt_now}_005930_stock.csv', index=True)

def stock_xy():
    dt_now = get_today()
    nexon = pd.read_csv(f'./{dt_now}_005930_stock.csv', index_col=0)
    scaler = MinMaxScaler()
    scaler2 = MinMaxScaler()
    scale_cols_for_x = ['시가', '고가', '저가', '거래량']
    scale_cols_for_y = ['종가']
    test = scaler.fit_transform(nexon[scale_cols_for_x])
    test2 = scaler2.fit_transform(nexon[scale_cols_for_y])
    np.save(f'./{dt_now}_test.npy', test)
    np.save(f'./{dt_now}_test2.npy', test2)
    
       
def lstm_stock(today_info):
    dt_now = get_today()
    test = np.load(f'./{dt_now}_test.npy')
    test2 = np.load(f'./{dt_now}_test2.npy')
    X = np.array([test[i:i+1] for i in range(test.shape[0]-1 )])
    y = np.array([test2[i+1] for i in range(test2.shape[0]-1)])
    X_model_input = tf.keras.layers.Input(shape=(X.shape[1], X.shape[2]))
    X_model_output = tf.keras.layers.LSTM(32, activation='relu', return_sequences=False)(X_model_input)
    X_model_output = tf.keras.layers.Dense(1, activation='linear')(X_model_output)
    X_model_output = tf.keras.layers.Dense(1)(X_model_output)
    x_train, x_valid, y_train, y_valid = train_test_split(X, y, test_size = 0.2) 
    result_model = tf.keras.Model(inputs=X_model_input, outputs=X_model_output)
    result_model.compile(optimizer='adam', loss='mean_squared_error', metrics=['acc'])
    early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)
    result_model.fit(x_train, y_train, batch_size = 1, epochs=100, validation_data=(x_valid, y_valid), callbacks=[early_stop])                
    pred = result_model.predict(np.array([today_info]))
    return pred

def predict_or_check(**kwargs):
    dt_now = get_today()
    nexon = pd.read_csv(f'./{dt_now}_005930_stock.csv', index_col=0)
    scaler = MinMaxScaler()
    scaler2 = MinMaxScaler()
    scale_cols_for_x = ['시가', '고가', '저가', '거래량']
    scale_cols_for_y = ['종가']
    scaler.fit_transform(nexon[scale_cols_for_x])
    scaler2.fit_transform(nexon[scale_cols_for_y])

    kst = pendulum.timezone('Asia/Seoul')
    current_time = datetime.now().astimezone(kst)

    today_ticker = stock.get_market_ohlcv(dt_now, dt_now, '005930')
    today_info = scaler.transform([[today_ticker['시가'].values[0], today_ticker['고가'].values[0], today_ticker['저가'].values[0], today_ticker['거래량'].values[0]]])
    test = lstm_stock(today_info=today_info)
    tomorrow_pred = scaler2.inverse_transform(test)
    tomorrow_pred = int(round(tomorrow_pred[0][0]))
    today_close = today_ticker['종가'].values[0]
    ti = kwargs['ti']
    ti.xcom_push(key=f'tomorrow_005930_pred', value=int(tomorrow_pred))
    ti.xcom_push(key=f'today_005930_close', value=int(today_close))
    print(tomorrow_pred, today_close)

def finish(**kwargs):
    ti = kwargs['ti']
    new_info = {
        'samsung' : ti.xcom_pull(task_ids='predict_samsung_task', key='tomorrow__005930_close'),
        'samsung_lstm': ti.xcom_pull(task_ids='predict_samsung_task', key='today_005930_pred'),
    }
    create_url = back_url + "/createstock"
    response = requests.post(create_url, json=new_info)
    response.raise_for_status()

def revise():
    kst = pendulum.timezone('Asia/Seoul')   
    current_time = datetime.now().astimezone(kst)
    dt_now = str(current_time.date())

    all_user_url = back_url + '/all'
    all_user = requests.get(all_user_url)
    get_stock_url = back_url + '/getstock'
    today_stock = requests.get(get_stock_url, params={'date': dt_now })

    for user in all_user["users"]:
        revise_url = back_url + f"/revise/{user['user_id']}"
        delta = int(round(1 / abs(today_stock['samsung'] - user['prediction']))) * 1000
        user_info = {
            'user_name': user['user_name'],
            'age': user['age'],
            'score': user['score'] + delta,
            'prediction': user['prediction'],
            'delta': delta,
        }
        response = requests.put(revise_url, params={'user_id': user['user_id']}, json=user_info)
