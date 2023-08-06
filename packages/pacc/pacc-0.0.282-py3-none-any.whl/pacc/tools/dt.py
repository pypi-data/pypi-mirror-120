from datetime import datetime


def showDatetime(text='now'):
    print("%s : %s" % (text, datetime.now()))
