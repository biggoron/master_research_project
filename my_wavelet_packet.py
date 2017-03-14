import math as math
import matplotlib.pyplot as plt
from scipy import fftpack as sp_fft
import numpy as np
from my_signal import *
import math as math
import pywt

class MyWavelet:
  # Symbolizes a wavelet decomposition
  def __init__(self, frame):
    # The tree
    self.wp = pywt.WaveletPacket(data=frame, wavelet='db6', mode='sym')
    self.max_level = self.wp.maxlevel
    self.data = {}
    self.entropy = {}
    root_entropy = MyWavelet.entropy(sp_fft.dct(self.wp.data))
    for i in range(self.max_level):
      nb = pow(2, i + 1)
      nodes = []
      for j in range(nb):
        index = '{0:b}'.format(j).replace('0', 'a').replace('1', 'd')
        index = 'a' * (i + 1 - len(index)) + index
        self.data[index] = sp_fft.dct(self.wp[index].data)
        self.entropy[index] = MyWavelet.entropy(self.data[index]) / root_entropy

  @staticmethod
  def best_basis(wp):
    entropy = {}
    basis = []
    for k in range(wp.max_level):
      for j in range(pow(2, k + 1)):
        index = '{0:b}'.format(j).replace('0', 'a').replace('1', 'd')
        index = 'a' * (k + 1 - len(index)) + index
        entropy[index] = wp.entropy[index]
        if len(index) == wp.max_level:
          basis.append(index)
      
    for j in range(wp.max_level - 1):
      k = wp.max_level - j
      for l in range(pow(2, k)):
        v = '{0:b}'.format(l).replace('0', 'a').replace('1', 'd')
        v = 'a' * (k - len(v)) + v
        if v[-1] == 'a':
          conj = v[:-1]
          conj = conj + 'd'
          if entropy[v] + entropy[conj] >= entropy[v[:-1]]:
            basis.append(v[:-1])
            for m in range(wp.max_level + 1 - len(v)):
              for n in range(pow(2, m + 1)):
                w = '{0:b}'.format(n).replace('0', 'a').replace('1', 'd')
                w = 'a' * (m + 1 - len(w)) + w
                w = v[:-1] + w
                if w in basis:
                  basis.remove(w)
          else:
            entropy[v[:-1]] = entropy[v] + entropy[conj]
    basis.sort()
    return basis
    
  @staticmethod
  def entropy(array):
    ent = 0
    for v in array:
      v2 = pow(v, 2)
      ent += v2 * math.log(0.00001 + v2)
    return - ent

  def all_features_at(p):

  def features_at(p):

  def all_features:

  def features:
    
    
    
