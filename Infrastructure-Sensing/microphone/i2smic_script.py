from scipy.io.wavfile import read
import numpy

a = read("file.wav")
numpy.array(a[1],dtype=float)
for i in a[1]:
    print(i)