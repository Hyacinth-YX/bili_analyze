import datetime
def timestamp2str(timestamp):
    return datetime.datetime.fromtimestamp (timestamp).strftime ("%Y--%m--%d %H:%M:%S")