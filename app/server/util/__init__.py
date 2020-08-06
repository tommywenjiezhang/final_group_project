from hashlib import sha224
from datetime import datetime
import pytz
import re
import os
def hashIdandTitle(title,id):
    raw = title + str(id)
    return sha224(raw.encode('utf-8')).hexdigest()

def todayandnow():
    return datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')

def combinUrl(params):
    baseUrl = os.environ.get('LOCAL_BASE_URL')
    return baseUrl + str(params)


def extractNumber(phoneNumberString):
    newString = re.sub('[^A-Za-z0-9]+', '', phoneNumberString)
    phoneNumber = re.compile(r'(\d+)', re.VERBOSE | re.IGNORECASE)
    mn = phoneNumber.match(newString)
    if mn:
        value = mn.group(0)
        return int(value)


if __name__ == "__main__":
    print("enter your number")
    phoneNumber = input()
    result =  extractNumber(phoneNumber)
    print(result)