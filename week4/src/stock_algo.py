from datetime import timedelta, datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from pykrx import stock
from statsmodels.tsa.arima_model import ARIMA

def get_today(): #오늘 날짜 받아오기
    dt_now = str(datetime.now().date())
    print(f'{dt_now} 기준')
    dt_now = ''.join(c for c in dt_now if c not in '-')
    return dt_now

def get_market_fundamental(): #시장 정보 get
    dt_now = get_today()
    df = stock.get_market_fundamental_by_ticker(date=dt_now)
    print(df.head())
    df.to_csv(f'./{dt_now}_market_fundamental.csv', index = True)

def get_nexon_stock():
    dt_now = get_today()
    nexon = stock.get_market_ohlcv("20150925", dt_now, "225570")
    print(nexon.head)
    nexon.to_csv(f'./{dt_now}_nexon_stock.csv', index=True)

def normalization():
    dt_now = get_today()
    df = pd.read_csv(f'./{dt_now}_nexon_stock.csv', index_col = 0)
    nexon = df[['종가']]
    scaler = MinMaxScaler()
    nexon = scaler.fit_transform(nexon)
    nexon.to_csv(f'./{dt_now}_nexon_normalization.csv', index_col = 0)

def create_dataset():
    dt_now = get_today()
    nexon = pd.read_csv(f'./{dt_now}_nexon_normalization.csv', index_col = 0)
    X = []
    Y = []
    for i in range(60, len(nexon)):
        X.append(nexon[i-60:i, 0])
        Y.append(nexon[i, 0])
    X, Y = np.array(X), np.array(Y)
    X.to_csv(f'./{dt_now}_X.csv', index_col = 0)
    Y.to_csv(f'./{dt_now}_Y.csv', index_col = 0)


def reshape_and_learning(setdate):
    dt_now = get_today()
    X = pd.read_csv(f'./{dt_now}_X.csv', index_col = 0)
    Y = pd.read_csv(f'./{dt_now}_Y.csv', index_col = 0)
    split = int(0.8 * len(X))
    X_train, Y_train = X[:split], Y[:split]
    X_test, Y_test = X[split:], Y[split:]
    #3차원으로 reshape
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(50))
    model.add(Dropout(0.2))
    model.add(Dense(1))

    model.complie(optimizer='adam', loss = 'mean_squared_erro') 

    history = model.fit(X_train, Y_train, epochs = 50, batch_size=32, validation_data=(X_test,Y_test))
    model = ARIMA(nexon['종가'], order = (2, 2, 2))
    model_fit = model.fit(disp=0)
    print(model_fit.summary())

    forecast = model_fit.forecast(steps=setdate)
    return forecast

def forecast():
    dt_now = get_today()
    print(f'{dt_now} 다음 날의 주가는? {reshape_and_learning(1)}')



# #필요한 변수만 선택
# nexon = nexon[['종가']]
# #데이터 정규화
# scaler = MinMaxScaler()
# nexon = scaler.fit_transform(nexon)
# #데이터셋 생성
# X = []
# Y = []
# for i in range(60, len(nexon)):
#     X.append(nexon[i-60:i, 0])
#     Y.append(nexon[i, 0])
# X, Y = np.array(X), np.array(Y)
# #train/test set 분리
# split = int(0.8 * len(X))
# X_train, Y_train = X[:split], Y[:split]
# X_test, Y_test = X[split:], Y[split:]
# #3차원으로 reshape
# X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
# X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# #LSTM 모델 생성
# model = Sequential()
# model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
# model.add(Dropout(0.2))
# model.add(LSTM(50, return_sequences=True))
# model.add(Dropout(0.2))
# model.add(LSTM(50, return_sequences=True))
# model.add(Dropout(0.2))
# model.add(LSTM(50))
# model.add(Dropout(0.2))
# model.add(Dense(1))

# model.complie(optimizer='adam', loss = 'mean_squared_erro')

# history = model.fit(X_train, Y_train, epochs = 50, batch_size=32, validation_data=(X_test,Y_test))

# model = ARIMA(nexon['종가'], order = (2, 2, 2))
# model_fit = model.fit(disp=0)
# print(model_fit.summary())
# forecast = model_fit.forecast(steps=1)
# print(forecast)
