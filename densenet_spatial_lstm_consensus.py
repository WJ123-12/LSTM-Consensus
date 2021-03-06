import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--process', help='Process', default='train')
parser.add_argument('-data', '--dataset', help='Dataset', default='ucf101')
parser.add_argument('-b', '--batch', help='Batch size', default=16, type=int)
parser.add_argument('-c', '--classes', help='Number of classes', default=101, type=int)
parser.add_argument('-e', '--epoch', help='Number of epochs', default=20, type=int)
parser.add_argument('-r', '--retrain', help='Number of old epochs when retrain', default=0, type=int)
parser.add_argument('-cross', '--cross', help='Cross fold', default=1, type=int)
parser.add_argument('-s', '--summary', help='Show model', default=0, type=int)
parser.add_argument('-lr', '--lr', help='Learning rate', default=1e-3, type=float)
parser.add_argument('-decay', '--decay', help='Decay', default=1e-6, type=float)
parser.add_argument('-model', '--model', help='Model DenseNet', default=121, type=int)
parser.add_argument('-n', '--neural', help='Neural number LSTM', default=128, type=int)
args = parser.parse_args()
print args

import sys
import config
import models
from keras import optimizers

process = args.process
if process == 'train':
    train = True
    retrain = False
    old_epochs = 0
elif process == 'retrain':
    train = True
    retrain = True
    old_epochs = args.retrain
else:
    train = False
    retrain = False

batch_size = args.batch
classes = args.classes
epochs = args.epoch
cross_index = args.cross
dataset = args.dataset
n_neurons = args.neural
pre_file = 'dense{}_spatial_lstm{}_consensus'.format(args.model,n_neurons)

seq_len = 3
dropout = 0.5

if train & (not retrain):
    weights = 'imagenet'
else:
    weights = None

result_model = models.DenseNetSpatialLSTMConsensus(
                    n_neurons=n_neurons, seq_len=seq_len, classes=classes, weights=weights, dropout=dropout, id=args.model)

if (args.summary == 1):
    result_model.summary()
    sys.exit()

lr = args.lr 
decay = args.decay
result_model.compile(loss='categorical_crossentropy',
                     optimizer=optimizers.SGD(lr=lr, decay=decay, momentum=0.9, nesterov=True),
                     metrics=['accuracy'])

if train:
    models.train_process(result_model, pre_file, data_type=[0], epochs=epochs, dataset=dataset,
        retrain=retrain,  classes=classes, cross_index=cross_index, 
        seq_len=seq_len, old_epochs=old_epochs, batch_size=batch_size)
else:
    models.test_process(result_model, pre_file, data_type=[0], epochs=epochs, dataset=dataset,
        classes=classes, cross_index=cross_index,
        seq_len=seq_len, batch_size=batch_size)
    
