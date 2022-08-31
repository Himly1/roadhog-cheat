from datetime import datetime

def asTimestampOfNow():
    (dt, micro) = datetime.utcnow().strftime('%Y%m%d%H%M%S.%f').split('.')
    return "%s%03d" % (dt, int(micro) / 1000)