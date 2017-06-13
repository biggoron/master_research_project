from __future__ import print_function
import collections
import math
import numpy as np
import os
import random
import tensorflow as tf
import zipfile
from matplotlib import pylab
from six.moves import range
from six.moves.urllib.request import urlretrieve
from sklearn.manifold import TSNE
from my_signal import *

raw_file = 'data/long/PereGoriot.raw'
raw_name = 'PereGoriot'

sig = MySignal(raw_file)

print(sig.length)


