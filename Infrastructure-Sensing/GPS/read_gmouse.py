import os
from subprocess import run

def read_coordinates():
    # run GPS data
    command = "cgps -s"
    os.system(command)