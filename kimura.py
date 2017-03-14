from my_sound import *
from my_signal import *
import numpy as np
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import pywt
import matplotlib.pyplot as plt
import matplotlib.cm as cm

class Phonem:
  def __init__(self, wav_name, b = None, e = None, draw = False, dt = 0.005):

    so = MySound.from_kimura(wav_name)
    si = MySignal.from_sound(so)
    if (b != None and e != None):
      si = MySignal.from_signal(si.signal[b:e])
    if draw:
      si.draw()
    self.signal = si
    self.f = si.features(dt)
    self.w = si.features(dt, mfcc=False, wav=True)
    self.fw = si.features(dt, wav=True)

  def reduce_dim_f(self, pca):
    x = []
    y = []
    for data in pca.transform(self.f):
      x.append(data[0])
      y.append(data[1])
    return x, y

  def reduce_dim_w(self, pca):
    x = []
    y = []
    for data in pca.transform(self.w):
      x.append(data[0])
      y.append(data[1])
    return x, y

  def reduce_dim_fw(self, pca):
    x = []
    y = []
    for data in pca.transform(self.fw):
      x.append(data[0])
      y.append(data[1])
    return x, y

  @staticmethod
  def get_p():
    p = np.array([])
    p = np.append(p, Phonem("C01_p1_01", b=3000, e=8000))
    p = np.append(p, Phonem("C01_p1_02", b=3000, e=8000))
    p = np.append(p, Phonem("C01_p1_03", b=3000, e=8000))
    p = np.append(p, Phonem("C01_p1_04", b=3000, e=8000))
    p = np.append(p, Phonem("C01_p1_05", b=3000, e=8000))
    p = np.append(p, Phonem("C01_p1_06", b=3000, e=8000))
    p = np.append(p, Phonem("C01_p1_07", b=3000, e=8000))
    p = np.append(p, Phonem("C01_p1_08", b=3000, e=8000))
    p = np.append(p, Phonem("C01_p1_09", b=3000, e=8000))
    return p

  @staticmethod
  def get_ph():
    ph = np.array([])
    ph = np.append(ph, Phonem("C02_p2_01", b=2500, e=7500))
    ph = np.append(ph, Phonem("C02_p2_02", b=2500, e=7500))
    ph = np.append(ph, Phonem("C02_p2_03", b=2500, e=7500))
    ph = np.append(ph, Phonem("C02_p2_04", b=2500, e=7500))
    ph = np.append(ph, Phonem("C02_p2_05", b=2500, e=7500))
    ph = np.append(ph, Phonem("C02_p2_06", b=2500, e=7500))
    ph = np.append(ph, Phonem("C02_p2_07", b=2500, e=7500))
    ph = np.append(ph, Phonem("C02_p2_08", b=2500, e=7500))
    ph = np.append(ph, Phonem("C02_p2_09", b=2500, e=7500))
    return ph

  @staticmethod
  def get_t():
    t = np.array([])
    t = t.append(t, Phonem("C25_t1_01", b=3500, e=8500))
    t = t.append(t, Phonem("C25_t1_02", b=3500, e=8500))
    t = t.append(t, Phonem("C25_t1_03", b=3500, e=8500))
    t = t.append(t, Phonem("C25_t1_04", b=3500, e=8500))
    t = t.append(t, Phonem("C25_t1_05", b=3500, e=8500))
    t = t.append(t, Phonem("C25_t1_06", b=3500, e=8500))
    t = t.append(t, Phonem("C25_t1_07", b=3500, e=8500))
    t = t.append(t, Phonem("C25_t1_08", b=3500, e=8500))
    t = t.append(t, Phonem("C25_t1_09", b=3500, e=8500))
    return t

  @staticmethod
  def get_h():
    h = np.array([])
    h = np.append(h, Phonem("C02_p2_01", b=3000, e=8000))
    h = np.append(h, Phonem("C02_p2_02", b=3000, e=8000))
    h = np.append(h, Phonem("C02_p2_03", b=3000, e=8000))
    h = np.append(h, Phonem("C02_p2_04", b=3000, e=8000))
    h = np.append(h, Phonem("C02_p2_05", b=3000, e=8000))
    h = np.append(h, Phonem("C02_p2_06", b=3000, e=8000))
    h = np.append(h, Phonem("C02_p2_07", b=3000, e=8000))
    h = np.append(h, Phonem("C02_p2_08", b=3000, e=8000))
    h = np.append(h, Phonem("C02_p2_09", b=3000, e=8000))
    return h

def train_pca_f(phonems, n = 2):
  data = np.array(phonems.pop().f)
  while len(phonems) != 0:
    data = np.append(data, phonems.pop().f, axis = 0)
  
  pca = PCA(n_components=n)
  pca.fit(data)
  return pca

def train_pca_w(phonems, n = 2):
  data = np.array(phonems[0].w)
  for i in range(1, len(phonems)):
    data = np.append(data, phonems[i].w, axis=0)
  pca = PCA(n_components=n)
  pca.fit(data)
  return pca

def train_pca_fw(phonems, n = 2):
  data = np.array(phonems.pop().fw)
  while len(phonems) != 0:
    data = np.append(data, phonems.pop().fw, axis = 0)
  
  pca = PCA(n_components=n)
  pca.fit(data)
  return pca

def train_lda_f(phonems, n = 2):
  data = np.array(phonems.pop().f)
  while len(phonems) != 0:
    data = np.append(data, phonems.pop().f, axis = 0)
  
  lda = LinearDiscriminantAnalysis(n_components=n)
  lda.fit(data)
  return lda

def train_lda_w(phonems, n = 2):
  data = np.array(phonems.pop().w)
  while len(phonems) != 0:
    data = np.append(data, phonems.pop().w, axis = 0)
  
  lda = LinearDiscriminantAnalysis(n_components=n)
  lda.fit(data)
  return lda

def train_lda_fw(phonems, n = 2):
  data = np.array(phonems.pop().fw)
  while len(phonems) != 0:
    data = np.append(data, phonems.pop().fw, axis = 0)
  
  lda = LinearDiscriminantAnalysis(n_components=n)
  lda.fit(data)
  return lda

class Experience:
  @classmethod
  def compare_p_ph(cls, time=False):
    p = Phonem.get_p()
    ph = Phonem.get_ph()
    
    p_train = p[:3]
    ph_train = ph[:3]
    
    train_set = np.append(p_train, ph_train)
    pca = train_pca_w(train_set, 2)
    
    px = []
    py = []
    for i in range(0, 9):
      x, y = p[i].reduce_dim_w(pca)
      px.append(x)
      py.append(y)
    
    phx = []
    phy = []
    for i in range(0, 9):
      x, y = ph[i].reduce_dim_w(pca)
      phx.append(x)
      phy.append(y)
    
    for i in range(0, 9):
      plt.scatter(px[i], py[i], c='white', cmap=cm.brg)
      plt.scatter(phx[i], phy[i], c='red', cmap=cm.brg)
    plt.title('apa and apha(red) represented in a base optized for 3 sounds apa and 3 sounds apha')
    plt.xlabel('feature 1')
    plt.ylabel('feature 2')
    #plt.colorbar()
    plt.show()
    plt.clf()

Experience.compare_p_ph()
        

#p[0].signal.draw()

#t = Phonem.get_t()

#h = Phonem.get_h()

#pca_f = train_pca_f([p, p2, p3, ph, ph2, ph3], 3)
#
#
#pca_h = train_pca_f([h, h2, h3, h4, h5, h6, h7, h8, h9], 2)
#
#hx, hy = h.reduce_dim_w(pca)
#hx2, hy2 = h2.reduce_dim_f(pca_h)
#hx3, hy3 = h3.reduce_dim_f(pca_h)
#hx4, hy4 = h4.reduce_dim_f(pca_h)
#hx5, hy5 = h5.reduce_dim_f(pca_h)
#hx6, hy6 = h6.reduce_dim_f(pca_h)
#hx7, hy7 = h7.reduce_dim_f(pca_h)
#hx8, hy8 = h8.reduce_dim_f(pca_h)
#hx9, hy9 = h9.reduce_dim_f(pca_h)
#
#t = np.arange(len(hx))
#
#plt.scatter(hx, hy, c=t, cmap=cm.brg)
#plt.scatter(hx2, hy2, c=t, cmap=cm.brg)
#plt.scatter(hx3, hy3, c=t, cmap=cm.brg)
#plt.scatter(hx4, hy4, c=t, cmap=cm.brg)
#plt.scatter(hx5, hy5, c=t, cmap=cm.brg)
#plt.scatter(hx6, hy6, c=t, cmap=cm.brg)
#plt.scatter(hx7, hy7, c=t, cmap=cm.brg)
#plt.scatter(hx8, hy8, c=t, cmap=cm.brg)
#plt.scatter(hx9, hy9, c=t, cmap=cm.brg)

#tx, ty = t.reduce_dim_w(pca)
#tx2, ty2 = t2.reduce_dim_w(pca)
#tx3, ty3 = t3.reduce_dim_w(pca)
#tx4, ty4 = t4.reduce_dim_w(pca)
#tx5, ty5 = t5.reduce_dim_w(pca)
#tx6, ty6 = t6.reduce_dim_w(pca)
#tx7, ty7 = t7.reduce_dim_w(pca)
#tx8, ty8 = t8.reduce_dim_w(pca)
#tx9, ty9 = t9.reduce_dim_w(pca)

#px2, py2 = p2.reduce_dim_w(pca)
#px3, py3 = p3.reduce_dim_w(pca)
#px4, py4 = p4.reduce_dim_w(pca)
#px5, py5 = p5.reduce_dim_w(pca)
#px6, py6 = p6.reduce_dim_w(pca)
#px7, py7 = p7.reduce_dim_w(pca)
#px8, py8 = p8.reduce_dim_w(pca)
#px9, py9 = p9.reduce_dim_w(pca)


#u = np.arange(len(phx))

#plt.scatter(px2, py2, c='white', cmap=cm.brg)
#plt.scatter(px3, py3, c='white', cmap=cm.brg)
#plt.scatter(px4, py4, c='white', cmap=cm.brg)
#plt.scatter(px5, py5, c='white', cmap=cm.brg)
#plt.scatter(px6, py6, c='white', cmap=cm.brg)
#plt.scatter(px7, py7, c='white', cmap=cm.brg)
#plt.scatter(px8, py8, c='white', cmap=cm.brg)
#plt.scatter(px9, py9, c='white', cmap=cm.brg)
#plt.scatter(tx, ty, c='red', cmap=cm.brg)
#plt.scatter(tx2, ty2, c='red', cmap=cm.brg)
#plt.scatter(tx3, ty3, c='red', cmap=cm.brg)
#plt.scatter(tx4, ty4, c='red', cmap=cm.brg)
#plt.scatter(tx5, ty5, c='green', cmap=cm.brg)
#plt.scatter(tx6, ty6, c='red', cmap=cm.brg)
#plt.scatter(tx7, ty7, c='red', cmap=cm.brg)
#plt.scatter(tx8, ty8, c='red', cmap=cm.brg)
#plt.scatter(tx9, ty9, c='red', cmap=cm.brg)
#plt.scatter(phx2, phy2, c='red', cmap=cm.brg)
#plt.scatter(phx3, phy3, c='red', cmap=cm.brg)
#plt.scatter(phx4, phy4, c='red', cmap=cm.brg)
#plt.scatter(phx5, phy5, c='red', cmap=cm.brg)
#plt.scatter(phx6, phy6, c='red', cmap=cm.brg)
#plt.scatter(phx7, phy7, c='red', cmap=cm.brg)
#plt.scatter(phx8, phy8, c='red', cmap=cm.brg)
#plt.scatter(phx9, phy9, c='red', cmap=cm.brg)
