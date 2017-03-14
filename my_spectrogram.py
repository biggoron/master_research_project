import math as math
import pywt
import numpy as np
import scikits.talkbox.features as tkbox
from scipy import fftpack as sp_fft
from my_wavelet import *
from my_sound import *
from my_features import *
from my_signal import *

class MySignal:

  def __init__(self, signal, w, overlap = 0.5, boundary = "zero"): 
    # TODO: Should return a Spectrogram object inheriting from Features
    # TODO: check 0 <= overlap <= 1
    spectrogram = np.array([])
    l = len(signal.signal)
    step = int(2 * w * (1 - overlap) + 1)
    print step
    sampling = signal.sampling * step
    signal_copy = signal.signal
    print len(signal_copy)
    # TODO: implement symetric padding
    # TODO: implement periodic padding
    # TODO: implement smoothed padding
    padding = np.zeros(w)
    signal_copy = np.concatenate((np.concatenate((padding, signal_copy)), padding))
    print len(signal_copy)
    print signal_copy
    for t in xrange(w, l + w - 1, step):
      window = MySignal.window(signal_copy, t, w) # default is hamming
      # -----------------------------------
      fft = np.fft.rfft(window.tolist())
      power_fft = np.array([])
      for f in fft:
        power_fft = np.append(power_fft, [abs(f)])
      # -----------------------------------
      if len(spectrogram) == 0:
        spectrogram = [power_fft]
      else:
        spectrogram = np.append(spectrogram, [power_fft], axis=0)
      self.signal = spectrogram
    return np.array(spectrogram)

