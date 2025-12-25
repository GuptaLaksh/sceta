import pandas as pd

def TimeStampFunc():

    timestamp = pd.Timestamp.now()
    timestamp_str = timestamp.strftime("_%y.%m.%d_%H.%M.%S")
    return timestamp_str

