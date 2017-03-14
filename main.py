from my_signal import *
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

example = MySignal("./data/raw/S1_SP210_bousou.raw")
print """
  there is %d wavelets coeffs
  there is %d mfcc coeffs
""" % (len(example.wv_coeffs), len(example.mfcc_coeffs[0]))

# Get the scalogram
# wavelet_dec = example.wavedec()
# wavelet_dec.print_scalogram()
features = []
for i in range(example.length):
  features.append(example.features(i))

print len(features)
print len(features[0])
print len(features[2])

#for f in features:
  #plt.plot(f)
  #plt.show()

# Apparently most of the information in on 5D
pca = PCA()
pca.fit(features)
#variances = pca.explained_variance_ratio_
#for i in range(len(variances)):
  #print variances[i]
Y = pca.fit_transform(features)

for nb_f in range(len(Y[0])):
  f = [Y[i][nb_f] for i in range(len(Y))]
  plt.plot(f)

plt.show()
