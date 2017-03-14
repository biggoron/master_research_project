from my_wavelet import *
from my_signal import *

p = MySignal.from_sound(MySound.from_kimura("C01_p1_01"))
f = p.features(mfcc = False, wav = True)
print f

