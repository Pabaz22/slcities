import pandas as pd
import numpy as np


def night_length(day):
    hlist=day.split(':')
    H,M,S = hlist
    day_light = int(H)*3600 + int(M)*60 + int(S)
    return 24*3600 - day_light
