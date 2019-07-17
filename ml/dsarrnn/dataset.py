import numpy as np
import pandas as pd
import math


def create_data_frame(csv_name):
    column_names = ["date", "time", "Open", "High", "Low", "Close", "Volume"]

    data_frame = pd.read_csv(csv_name, names=column_names)
    data_frame['Date'] = data_frame.date + ' ' + data_frame.time
    data_frame.Date = pd.to_datetime(data_frame.Date, format="%Y.%m.%d %H:%M")

    stock_frame = pd.DataFrame()

    stock_frame['Date'] = data_frame.Date
    stock_frame['Open'] = data_frame.Open
    stock_frame['High'] = data_frame.High
    stock_frame['Low'] = data_frame.Low
    stock_frame['Close'] = data_frame.Close
    stock_frame['Adj Close'] = data_frame.Close
    stock_frame['Volume'] = data_frame.Volume

    return stock_frame


class Dataset:

    def __init__(self, driving_csv, target_csv, T, split_ratio=0.8, normalized=False):

        stock_frame1 = create_data_frame(driving_csv)
        stock_frame2 = create_data_frame(target_csv)

        print(stock_frame1.head())
        print(stock_frame2.head())

        if stock_frame1.shape[0] > stock_frame2.shape[0]:
            stock_frame1 = self.crop_stock(stock_frame1, stock_frame2['Date'][0]).reset_index()
        else:
            stock_frame2 = self.crop_stock(stock_frame2, stock_frame1['Date'][0]).reset_index()
        stock_frame1 = stock_frame1['Close'].fillna(method='pad')
        stock_frame2 = stock_frame2['Close'].fillna(method='pad')
        self.train_size = int(split_ratio * (stock_frame2.shape[0] - T - 1))
        self.test_size = stock_frame2.shape[0] - T - 1 - self.train_size
        if normalized:
            stock_frame2 = stock_frame2 - stock_frame2.mean()
        self.X, self.y, self.y_seq = self.time_series_gen(stock_frame1, stock_frame2, T)
        # self.X = self.percent_normalization(self.X)
        # self.y = self.percent_normalization(self.y)
        # self.y_seq = self.percent_normalization(self.y_seq)

    def get_size(self):
        return self.train_size, self.test_size

    def get_num_features(self):
        return self.X.shape[1]

    def get_train_set(self):
        return self.X[:self.train_size], self.y[:self.train_size], self.y_seq[:self.train_size]

    def get_test_set(self):
        return self.X[self.train_size:], self.y[self.train_size:], self.y_seq[self.train_size:]

    def time_series_gen(self, X, y, T):
        ts_x, ts_y, ts_y_seq = [], [], []
        for i in range(len(X) - T - 1):
            last = i + T
            ts_x.append(X[i: last])
            ts_y.append(y[last])
            ts_y_seq.append(y[i: last])
        return np.array(ts_x), np.array(ts_y), np.array(ts_y_seq)

    def crop_stock(self, df, date):
        start = df.loc[df['Date'] == date].index[0]
        return df[start:]

    def log_normalization(self, X):
        X_norm = np.zeros(X.shape[0])
        X_norm[0] = 0
        for i in range(1, X.shape[0]):
            X_norm[i] = math.log(X[i] / X[i - 1])
        return X_norm

    def percent_normalization(self, X):
        if len(X.shape) == 2:
            X_norm = np.zeros((X.shape[0], X.shape[1]))
            for i in range(1, X.shape[0]):
                X_norm[i, 0] = 0
                X_norm[i] = np.true_divide(X[i] - X[i - 1], X[i - 1])
        else:
            X_norm = np.zeros(X.shape[0])
            X_norm[0] = 0
            for i in range(1, X.shape[0]):
                X_norm[i] = (X[i] - X[i - 1]) / X[i]
        return X_norm
