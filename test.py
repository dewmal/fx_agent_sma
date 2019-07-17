from ml.dsarrnn import train
import os
dirname, filename = os.path.split(os.path.abspath(__file__))
print(dirname)

train.train(dirname)
