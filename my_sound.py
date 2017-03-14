import os
import re
import numpy as np
import matplotlib.pyplot as plt

class MySound:
  # Symbolizes a wav sound file
  # can be listen, transformed to raw, transformed to my_signal
  # can be printed

  def __init__(self, raw_file, inttype='<i2'):
    # Usage: builds a sound wrapper out of the name of a binary raw in data/raw
    # Builds a wrapper from a single file
    # The filename is assumed to be in data/wav
    self.formated = re.match(r".*S(\d*)_SP(\d*)_(\w*).raw", raw_file)
    f = open("./data/raw/%s" % raw_file, "r")
    try:
      self.raw = (np.fromfile(f, dtype=np.dtype(inttype)))
      #array.astype('int16').tofile(filename)
      (self.raw).astype(int)
    finally:
      f.close()

  @classmethod
  def from_wav(cls, wav_file, inttype='<i2'):
    # Usage: builds a sound wrapper out of the name of a wav file in data/wav
    # Stores a temporary binary version in data/raw/temp
    formated = re.match(r".*S(\d*)_SP(\d*)_(\w*).wav", wav_file)
    basename = formated.group(3)
    series = int(formated.group(1))
    speaker = int(formated.group(2))
    raw_name = cls.raw_fullname(basename, series, speaker)
    os.system('sox data/wav/%s -b 16 -e signed-integer -c 1 -r 16k -t raw ./data/raw/temp/%s' % (wav_file, raw_name))
    return cls('temp/%s' % raw_name)

  @classmethod
  def from_kimura(cls, wav, inttype='<i2'):
    os.system('sox data/wav/%s -b 16 -e signed-integer -c 1 -r 16k -t raw ./data/raw/temp/%s' % (wav + ".wav", wav + ".raw"))
    return cls('temp/%s' % wav + ".raw")
  
  @classmethod
  def from_raw(cls, raw_array, name, speaker = 0, series = 0):
    # Usage: builds a sound wrapper out of an array representing the signal
    # Stores a temporary binary version in data/raw/temp
    raw_name = cls.raw_fullname(name, series, speaker)
    raw_path = 'data/raw/temp/%s' % raw_name
    raw_array.astype('int16').tofile('data/raw/temp/%s' % raw_name)
    return cls('temp/%s' % raw_name)

  @classmethod
  def from_wav_dir(cls, directory = 'data/wav/'):
    # Create a sound wrapper for each of the wav files in a dir
    # returns an array of those
    sounds = []
    for filename in os.listdir(directory):
      if filename.endswith(".wav"):
        sounds.append(cls.from_wav(filename)) 
    return sounds

  def filename(self):
    # returns 'bousou' in 'data/raw/S1_SP104_bousou.raw
    if self.formated.group(3):
      return self.formated.group(3)
    else:
      return 0

  def series(self):
    # returns '1' in 'data/raw/S1_SP104_bousou.raw
    # gotcha: returns a string
    if self.formated.group(1):
      return self.formated.group(1)
    else:
      return 0

  def speaker(self):
    # returns '104' in 'data/raw/S1_SP104_bousou.raw
    # gotcha: returns a string
    if self.formated.group(2):
      return self.formated.group(2)
    else:
      return 0
    
  @staticmethod
  def convert_raw(raw_file, wav_path):
    # takes a raw file and converts it to wav
    os.system('sox -r 16k -e signed-integer -b 16 -c 1 %s %s' % (raw_file, wav_path))

  @staticmethod
  def wav_fullname(basename, series = 0, speaker = 0):
    # builds a standardized name S*series*_SP*speaker*_word.wav
    return "S%d_SP%d_%s.wav" % (series, speaker, basename)

  @staticmethod
  def raw_fullname(basename, series = 0, speaker = 0):
    # builds a standardized name S*series*_SP*speaker*_word.raw
    return "S%d_SP%d_%s.raw" % (series, speaker, basename)

  def wav_name(self):
    # Gives the standardized wav name of the current sound
    return "S%s_SP%s_%s.wav" % (self.series(), self.speaker(), self.filename())
  
  def raw_name(self):
    # Gives the standardized raw name of the current sound
    return "S%s_SP%s_%s.raw" % (self.series(), self.speaker(), self.filename())

  def save_raw(self, name = None):
    # saves a binary raw of the current sound in data/raw, the name can contain sub dir
    if name == None:
      name = self.raw_name()
    self.raw.astype('int16').tofile('data/raw/%s' % name)
    return 'data/raw/%s' % name

  def save_wav(self, name = None):
    # saves wav version of current sound in data/wav, the name can contain sub dir
    if name == None:
      wav_path = 'data/wav/%s' % self.wav_name()
    else:
      wav_path = 'data/wav/%s' % name
    raw_path = self.save_raw('temp/%s' % self.raw_name())
    MySound.convert_raw(raw_path, wav_path)

  def to_s(self):
    # returns the stringified data
    print self.raw.tolist()

  def draw(self):
    # plots the sound signal (simple plot)
    plt.plot(self.raw.tolist())
    plt.ylabel('amplitude')
    plt.xlabel('time 1/16000')
    plt.show()

  def play(self):
    # builds a wav version of the sound in data/wav/temp and plays it (linux only)
    os.system('play %s' % self.source)

  # TODO: to_signal method
