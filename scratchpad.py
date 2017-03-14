from my_sound import *
from my_signal import *
import numpy as np
from sklearn.decomposition import PCA
import pywt
import matplotlib.pyplot as plt

oosama_wav_name = MySound.wav_fullname('oosama', 1, 104)
oosama = MySound.from_wav(oosama_wav_name)

oosama_signal = MySignal.from_sound(oosama)
oosama_signal.compute_wavedec()
oosama_signal.compute_mfcc()

bousou_wav_name = MySound.wav_fullname('bousou', 1, 104)
bousou = MySound.from_wav(bousou_wav_name)

bousou_signal = MySignal.from_sound(bousou)
bousou_signal.compute_wavedec()
bousou_signal.compute_mfcc()

mukiuchi_wav_name = MySound.wav_fullname('mukiuchi', 1, 104)
mukiuchi = MySound.from_wav(mukiuchi_wav_name)

mukiuchi_signal = MySignal.from_sound(mukiuchi)
mukiuchi_signal.compute_wavedec()
mukiuchi_signal.compute_mfcc()
#mukiuchi_signal.draw()

yuubin_wav_name = MySound.wav_fullname('yuubin', 1, 104)
yuubin = MySound.from_wav(yuubin_wav_name)

yuubin_signal = MySignal.from_sound(yuubin)
yuubin_signal.compute_wavedec()
yuubin_signal.compute_mfcc()
#yuubin_signal.draw()

o = MySignal.from_signal(oosama_signal.signal[4000:5000])
a = MySignal.from_signal(oosama_signal.signal[10500:11500])
s = MySignal.from_signal(oosama_signal.signal[6600:7600])

ch = MySignal.from_signal(mukiuchi_signal.signal[11500:12500])

m = MySignal.from_signal(oosama_signal.signal[9250:9750])
m_bis = MySignal.from_signal(mukiuchi_signal.signal[3250:3750])

b = MySignal.from_signal(bousou_signal.signal[3400:3900])
b_bis = MySignal.from_signal(yuubin_signal.signal[8000:8500])

fo = o.features(0.005)
fa = a.features(0.005)
wo = o.features(0.005, mfcc=False, wav=True)
wa = a.features(0.005, mfcc=False, wav=True)
fwo = o.features(0.005, wav=True)
fwa = a.features(0.005, wav=True)

fm = np.append(m.features(0.005), m_bis.features(0.005), axis=0)
fs = s.features(0.005)
fch = ch.features(0.005)
b1 = b.features(0.005)
b2 = b_bis.features(0.005)
fb = np.append(b1, b2, axis=0)

m1 = m.features(0.005, mfcc=False, wav=True)
m2 = m_bis.features(0.005, mfcc=False, wav=True)
wm = np.append(m1, m2, axis=0)
ws = s.features(0.005, mfcc=False, wav=True)
wch = ch.features(0.005, mfcc=False, wav=True)
b1 = b.features(0.005, mfcc=False, wav=True)
b2 = b_bis.features(0.005, mfcc=False, wav=True)
wb = np.append(b1, b2, axis=0)

m1 = m.features(0.005, wav=True)
m2 = m_bis.features(0.005, wav=True)
fwm = np.append(m1, m2, axis=0)
fws = s.features(0.005, wav=True)
fwch = ch.features(0.005, wav=True)
b1 = b.features(0.005, wav=True)
b2 = b_bis.features(0.005, wav=True)
fwb = np.append(b1, b2, axis=0)

fall = np.append(fo, fa, axis=0)
wall = np.append(wo, wa, axis=0)
fwall = np.append(fwo, fwa, axis=0)

#cfall = np.append(fm, fb, axis=0)
#cwall = np.append(wm, wb, axis=0)
#cfwall = np.append(fwm, fwb, axis=0)

cfall = np.append(fs, fch, axis=0)
cwall = np.append(ws, wch, axis=0)
cfwall = np.append(fws, fwch, axis=0)

pca = PCA(n_components=2)
pca.fit(fall)
o_n = pca.transform(fo)
a_n = pca.transform(fa)

for data in o_n:
  x = data[0]
  y = data[1]
  plt.scatter(x, y, color="red")
for data in a_n:
  x = data[0]
  y = data[1]
  plt.scatter(x, y, color="blue")

#plt.show()

plt.clf()

pca = PCA(n_components=2)
pca.fit(cfall)
s_n = pca.transform(fs)
ch_n = pca.transform(fch)

for data in s_n:
  x = data[0]
  y = data[1]
  plt.scatter(x, y, color="red")
for data in ch_n:
  x = data[0]
  y = data[1]
  plt.scatter(x, y, color="blue")

plt.show()

plt.clf()

#plt.imshow(spec.tolist(), aspect="auto", interpolation='nearest', origin="lower")
#plt.show()

