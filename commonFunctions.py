import pandas as pd
import numpy as np


def PopupHorizontally(t):
    popupText = '<span style="white-space: nowrap;">' + t + '</span>'
    return popupText


def ReverseLatLon(locations):
    return [(p[1], p[0]) for p in locations]