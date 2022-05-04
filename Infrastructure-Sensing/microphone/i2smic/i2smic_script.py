from scipy.io.wavfile import read
import numpy
import os
from subprocess import run

# int sample_rate = 480
# str sample_rate_str = str(sample_rate)

def mic_init():
    output = run(["arecord", "-l"], capture_output=True).stdout
    
    return chr(output.split()[8][0])

def mic_read(mic_dev_num, time):
    print("Reading from microphone...\n")
    # Read data from sensor and store them into file.wav
    # -r sample rate (2000 -> 8kb in size, 480000 -> 1920044 b in size)
    # os.system("cd microphone/i2smic")
    command = "arecord -D plughw:" + mic_dev_num + " -c1 -r 480000 -f S32_LE -t wav -V mono -d " + str(time) + " audio.wav"
    os.system(command)

    # Read data from file.wav
    a = read("audio.wav")
    # Convert to numpy array
    # os.system("cd ../..")
    res = numpy.array(a[1],dtype=float)
    print("\nDone!\n")
    # print(res[0])
    return res
    
    # Save using numpy.savez
    # numpy.savez("audio.wav")
    # TODO: do something to stream data here
    # print("Pretend to be steaming data...\n")

    # Remove file.wav to save memory spae
    # os.system("rm file.wav")

