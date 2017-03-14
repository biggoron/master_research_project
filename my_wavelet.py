import numpy as np
import scipy.stats as sp
import pywt

class MyWavelet:
  # Symbolizes a wavelet decomposition
  def __init__(self, signal, wavelet_f, mode):
    db6 = pywt.Wavelet(wavelet_f)
    self.coeff = pywt.wavedec(signal, db6)

  def features(self):
    features = []
    for cs in self.coeff:
#      features.append(np.mean(cs))
      features.append(np.std(cs))
#      features.append(sp.skew(cs))
#      features.append(sp.kurtosis(cs))
    return features

  def mean_features(self):
    features = []
    for cs in self.coeff:
      features.append(np.mean(cs))
    return features
