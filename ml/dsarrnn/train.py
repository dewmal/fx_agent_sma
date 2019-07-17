import torch

from ml.dsarrnn.model import da_rnn
import utils.util as util
import matplotlib.pyplot as plt

global logger

util.setup_log()
# util.setup_path()
logger = util.logger

use_cuda = torch.cuda.is_available()
logger.info("Is CUDA available? %s.", use_cuda)


def train(io_dir):
    io_dir = f'{io_dir}/_data_'

    model = da_rnn(file_data='{}/nasdaq100_padding.csv'.format(io_dir), logger=logger, parallel=False,
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
