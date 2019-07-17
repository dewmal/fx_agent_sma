import torch
import pandas as pd
import numpy as np
from ml.dsarrnn.model import da_rnn
import utils.util as util
import matplotlib.pyplot as plt

global logger

util.setup_log()
# util.setup_path()
logger = util.logger

use_cuda = torch.cuda.is_available()
logger.info("Is CUDA available? %s.", use_cuda)


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


def train(io_dir):
    io_dir = f'{io_dir}/_data_'

    window_name = "M1"
    suffix = "201906"

    drive_data_frames = []
    drive_data_settings = []

    target_data_frame = None

    drive = ['EURAUD', 'EURCHF', 'EURGBP', 'EURJPY', 'USDCAD', 'USDCHF', 'USDJPY', 'CADCHF', 'EURCAD', 'EURNZD',
             'GBPJPY', 'GBPUSD']
    target = 'EURUSD'

    for p in [*drive, target]:
        path = f"{io_dir}/HISTDATA_COM_MT_{p}_{window_name}{suffix}/DAT_MT_{p}_{window_name}_{suffix}.csv"
        dp = create_data_frame(path)
        if p != target:
            drive_data_frames.append(dp)
        else:
            target_data_frame = dp
        drive_data_settings.append({"name": p, 'idx': 0})

    X = []
    Y = []
    for idx in range(len(target_data_frame)):
        t_date = target_data_frame.iloc[idx, 0]
        # print(t_date)

        values = []

        for idx_d, dp in enumerate(drive_data_frames):
            idx_saved = drive_data_settings[idx_d]['idx']
            d_date = dp.iloc[idx_saved, 0]
            if t_date >= d_date:
                drive_data_settings[idx_d]['idx'] = idx_saved + 1
                # values.append(dp.iloc[idx_saved, 1])
                # values.append(dp.iloc[idx_saved, 2])
                # values.append(dp.iloc[idx_saved, 3])
                values.append(dp.iloc[idx_saved, 4])

        if len(values) == len(drive) :
            # values = np.array(values)
            X.append(values)
            Y.append(target_data_frame.iloc[idx, 4])
            # print(f"{idx}")

    X = np.array(X)
    Y = np.array(Y)

    print(X.shape, Y.shape)

    model = da_rnn(X, Y, logger=logger, parallel=False,
                   learning_rate=.001)

    model.train(n_epochs=500)

    y_pred = model.predict()

    plt.figure()
    plt.semilogy(range(len(model.iter_losses)), model.iter_losses)
    plt.show()

    plt.figure()
    plt.semilogy(range(len(model.epoch_losses)), model.epoch_losses)
    plt.show()

    plt.figure()
    plt.plot(y_pred, label='Predicted')
    plt.plot(model.y[model.train_size:], label="True")
    plt.legend(loc='upper left')
    plt.show()
