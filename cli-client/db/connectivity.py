import urllib.request
from urllib.error import URLError

def connected( url ):
    try:
        ret = urllib.request.urlopen(url)
    except ( URLError, ValueError ) as e:
        return False
    if ret.code == 200:
        return True
    return False
