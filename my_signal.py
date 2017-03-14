import math as math
import pywt
import numpy as np
import scikits.talkbox.features as tkbox
from scipy import fftpack as sp_fft
from my_wavelet import MyWavelet
from my_sound import *

class MySignal:
  # TODO: get sampling up, then get the draw better
  # Symbolizes a signal
  # Interacts closely with Sound
  # Can produce some wavelet set, some mfcc set, or directly some features
  # Can be printed or even heard if inttype='<i2' is satisfied

  def __init__(self, filename, inttype='<i2', sampling=(1.0/16000)):
    # Directly builds a signal from a binary raw file
    self.sampling = sampling
    f = open(filename, "r")
    try:
      self.signal = (np.fromfile(f, dtype=np.dtype(inttype)))
      (self.signal).astype(int) 
      self.length = len(self.signal)
      
      self.wv_coeffs = None
      self.mfcc_coeffs = None
      #self.wv_coeffs = self.wavedec().coeffs # TODO: compute later
      #self.mfcc_coeffs = self.mfcc() # TODO: compute later
    finally:
      f.close()
      
  @classmethod
  def from_signal(cls, raw_array, name = None, speaker = 0, series = 0):
    # builds a signal from an array representing the signal
    # in practice, creates a temporary raw file in data/raw/temp and call basic constructor
    if name is None: # N:
      name = 'temp'
    raw_name = MySound.raw_fullname(name, series, speaker)
    raw_path = 'data/raw/temp/%s' % raw_name
    raw_array.astype('int16').tofile(raw_path)
    return cls(raw_path)

  @classmethod
  def from_sound(cls, sound, name = None):
    # Constructs a signal from a sound
    # uses the array representation of the sound
    obj = cls.from_signal(sound.raw, name)
    return obj

  # def normalize(self) # TODO: trim silences, align signal strength
    # then return new signal

  # Windowing functions
  @staticmethod
  def hamming(width):
    return np.hamming(1 + width*2)

  @staticmethod
  def window(sig, center, width, w_type = 'hamming'):
    # TODO: make a switch for other cases
    if w_type == 'hamming':
      w_array = MySignal.hamming(width)
    i = 0
    window = np.array([])
    for a in w_array:
      t = center - width + i
      window = np.append(window, [a * sig[t]])
      i += 1
    return window

  def fft(self, name = None):
    # fast fourier transform
    # return complex np array
    return np.fft.fft(self.signal.tolist())
    # Access imaginay and real with .real and .imag

  def ifft(self, name = None):
    # inverse fast fourier transform
    # return complex np array
    return np.fft.ifft(self.signal.tolist())
    # Access imaginay and real with .real and .imag

  def rfft(self, name = None):
    # Real to half hermitian
    return np.fft.rfft(self.signal.tolist())

  def irfft(self, name = None):
    # Half hermitian to real
    return np.fft.irfft(self.signal.tolist())

  def prfft(self):
    rfft = self.rfft()
    a = np.array([])
    for s in rfft:
      a = np.concatenate((a, [abs(s)]), axis = 0)
    return a

#  def spectrogram(self, w, overlap = 0.5, name = None, boundary = "zero"):
#    return MySpectrogram(self, w, overlap, boundary)

  def dct(self):
    # discrete cosine transform for the cepstral domain
    return sp_fft.dct(self.signal.tolist())

  def idct(self):
    # inverse discrete cosine transform 
    return sp_fft.idct(self.signal.tolist())

#  def wavedec(self, wavelet_f='db6', mode='sym'):
#    # wavelet decomposition, should return the appropriate object
#    return MyWavelet(self.signal, wavelet_f, mode)
#
#  def compute_wavedec(self, wavelet_f='db6', mode='sym'):
#    if self.wv_coeffs is None: # N:
#      self.wv_coeffs = self.wavedec(wavelet_f, mode)
#    return self.wv_coeffs

  def mfcc(self):
    # mfcc decomposition, should return the appropriate object
    coeffs, mspec, spec = tkbox.mfcc(self.signal)
    # TODO: create an object to wrap the coeffs and return that
    return coeffs

  def compute_mfcc(self):
    if self.mfcc_coeffs is None: # N:
      self.mfcc_coeffs = self.mfcc()
    return self.mfcc_coeffs

#  def features_at(self, i):
#    self.compute_mfcc()
#    self.compute_wavedec()
#    f = []
#    p = float(i) / float(self.length)
#    upper_w = p - math.floor(p)
#    lower_w = 1 - upper_w
#    # For wavelets:
#    for scale in range(len(self.wv_coeffs)):
#      j = math.floor(len(self.wv_coeffs[scale]) * p)
#      f.append(self.wv_coeffs[scale][int(j)])
#    j = math.floor(len(self.mfcc_coeffs) * p)
#    mfcc_i_coeffs = self.mfcc_coeffs[int(j)]
#    for c in mfcc_i_coeffs:
#      f.append(c)
#    return f

  def features(self, dt = 0.016, mfcc = True, wav = False):
    f = None
    self.compute_mfcc()
    m = np.array(self.mfcc_coeffs)
    ds = int(dt / self.sampling)
    for s in xrange(0, self.length, ds):
      if s + ds < self.length:
        g = np.array([])
        if mfcc:
          m_c = m[MySignal.interpolate(s, len(m), self.length)]
          g = np.append(g, m_c)
        if wav:
          window = self.signal[s:s + ds]
          w_c = MyWavelet(window, 'db6', 'sym')
          w_c = np.array(w_c.features())
          g = np.append(g, w_c)
        if f is None:
          f = np.array([g])
        else:
          f = np.append(f, np.array([g]), axis = 0)
    return f

  @staticmethod
  def interpolate(i, j, k):
    return int(i * float(j) / k )

  def draw(self):
    # simple plot
    plt.plot(self.signal.tolist())
    plt.ylabel('amplitude')
    plt.xlabel('time 1/16000')
    plt.show()

