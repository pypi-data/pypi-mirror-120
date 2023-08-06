from urllib.request import urlopen
from urllib.error import URLError, HTTPError

def htpp_status_check(requestURL):

    try:
        response = urlopen(requestURL)
        print('Status code : ' + str(response.code))
        print('Message : ' + 'Request succeeded. Request returned message - ' + response.reason)
    except HTTPError as e:
        print('Status : ' + str(e.code))
        print('Message : Request failed. Request returned reason - ' + e.reason)
    except URLError as e:
        print('Status :',  str(e.reason).split(']')[0].replace('[',''))
        print('Message : '+ str(e.reason).split(']')[1])
