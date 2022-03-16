from scipy.io.wavfile import read
import numpy
import os


print("Readind from microphone...\n")

# int sample_rate = 480
# str sample_rate_str = str(sample_rate)


while (1):
    # Read data from sensor and store them into file.wav
    # -r sample rate (2000 -> 8kb in size, 480000 -> 1920044 b in size)
    os.system("arecord -D plughw:0 -c1 -r 480000 -f S32_LE -t wav -V mono -d 1 file.wav")

    # Read data from file.wav
    a = read("file.wav")
    # Convert to numpy array
    # TODO: save using numpy.savez
    numpy.array(a[1],dtype=float)
    print("\nsize of file =", len(a[1]), "\n")
    # TODO: do something to stream data here

    # Remove file.wav to save memory spae
    os.system("rm file.wav")


    