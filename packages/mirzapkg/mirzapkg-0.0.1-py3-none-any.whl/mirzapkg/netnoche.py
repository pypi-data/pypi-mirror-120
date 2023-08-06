"""
Network
"""
import requests
import re




def get_tor_session():
    session = requests.session()
    session.proxies = {'http':  'socks5h://127.0.0.1:9050',
                       'https': 'socks5h://127.0.0.1:9050'}
    ret=""
    success="This browser is configured to use Tor"
    try:
        ret=session.get("https://check.torproject.org/").text
        if  success in ret:
            print("TorBala Got a session")
            return session
        else:
            print("deadend")
    except Exception as e:
        print(e)
    return session


def getHTML(url,secure=0):
    print(secure)
    session=""
    if secure>0:
        session=get_tor_session()
        print("Tor On:{}".format(url))
    elif secure<1 :
        session=requests.session()
        print("IRTCI:{}".format(url))
    try:
        return session.get(url).text  #content.capitalize()
    except Exception as e:
        print (e)
        return "[ERROR]"+str(e)

def myIP(session=requests.session()):
    """
    Stuborn function to extract callerIP for a passed sesssion.
    """
    provider =[ 'http://farbodfarjadi.rf.gd/',
                'https://www.cloudflare.com/cdn-cgi/trace',
                'https://idenrrt.me/',
                'http://icanhazip.com',
                'http://httpbin.org/ip',
                'http://checkip.amazonaws.com/']
    ret=[]

    for p in provider:
        res="2"
        try:

            # res = session.get(p).text
            print('trying : ' +p)
            res=getHTML(p)
            s=re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',res)
            ret.append(s)
        except Exception as e:
            ret.append(e.args)
    return ret
