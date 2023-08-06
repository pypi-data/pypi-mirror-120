#This is Noche, helper functions go in here. Khadang is for OOP funcations
#Noche is always dirty, Khadang is a good boy.
import re
import uuid
from urllib.request import urlopen
import time
from json import *
import requests
import re, string

###########

"""
Random Text helper
"""
def berin(n=0,sign='-'):
    s=sign
    for i in range(n):
        s=s+sign
        print(s)
    return s

###########

###############
"""
Text Processing
"""

###############
def sortedDict(words):
    count_dict = {}
    for w in words:
        count_dict[w] = words.count(w)
    return dict(sorted(count_dict.items(), key=lambda x:x[1]))

def countFrequency(my_list):

   # Creating an empty dictionary
   count = {}
   for i in my_list:
    count[i] = count.get(i, 0) + 1
   return count

def getIPfromstring(s):
    return re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',s)



def beCheloon(s):
    pattern=re.compile('([^\s\w-]|_)+')
    # pattern = re.compile('[\W]+')
    s=pattern.sub('', s)
    s=re.sub(r"[\n\t\r]*", "", s)
    return s
def beCheloon2(s):
    print(s)
    berin()
    extraSpace=re.compile(r'\s{2}')
    alphaNumericOnly=re.compile(r'\W\S')

    ss=alphaNumericOnly.sub(' ',s)
    print(ss)
    berin()
    sss=extraSpace.sub(' ', ss)
    print(sss)
    return sss
def tamiz(s):
    s=re.sub('\n+', ' ', s)

    s=re.sub('\r+', ' ', s)
    s=re.sub('\s+', ' ', s)
    return s

def cleanUp(s):
    s=re.sub('\n+', ' ', s).strip()
    s=re.sub('\r+', ' ', s).strip()
    return s


def read(address,retFormat=0):
    try:
        with  open (address, 'r', encoding='utf-8') as f :
            ret=f.read()
            if retFormat:
                return ret.split('\n')
            return ret
    except Exception as e:
        return str(e)

def giveMeRand():
    return uuid.uuid4()
def giveMeTNS():
    return  str(time.time_ns())
def esmBedeh(*args):
        """

        """
        name=giveMeTNS()+"."+str(giveMeRand())
        if args:
            name=name+"."+args[0]


        return name

def save(*args):
    """
        Save(content,extension,path,name) the 4th one can be combined into the third
    """
    content=args[0]
    name=esmBedeh()
    l=len(args)
    if  l==2:
        if '*' in args[1]:
            name=args[1].replace("*",name)
        else:
            name=args[1]
    try:
        with  open(name, "w+") as f:
            f.write(content)
        return name
    except Exception as e:
        return str(e)


#else:     url = 'https://ipinfo.io/' + addr + '/json'

def whoAmI():
    url = 'https://www.cloudflare.com/cdn-cgi/trace'
    session=requests.session()
    res = session.get(url).text
    ip=re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',res)
    #urlRE=re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',res)
    country=re.findall("loc=.*$",res,re.MULTILINE)
    return country[0].replace("loc=","")


def whereAmI():
    return whoAmI().upper()

def isItSafe():
    country=whereAmI()
    if(country=='IR'):
        return 0
    else:
        return 1
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
            res=getHTML(p)
            ret.append(re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',res))
        except Exception as e:
            ret.append(e.args)
    return ret


def clean(text,mode="normal"):
    pass
    #remove none alpha numeric






####### Bama Block Helper######
#ventlist car-ad-list-new clearfix
#search-new-marquee

def cleanFrontPage(s):
    try:

        i=s.find('ventlist car-ad-list-new clearfix') #
        i2=s.find('earch-new-marquee')
        return s[i:i2]
    except Exception as e:
        print (e)
        return str(e)
def cleanAgahiBama(s):
    """
    UGLYHACK
    Cuts the midle part of the ad page of
    just to make it easier on finding the
    data with BeautifulSoup.

    """
    try:

    #    i=s.find('<div class="prd-detail ad-detail-maindiv">')
        i=s.find('<section id="content" class="ad-detail-mob page-Advertisement-addetail">')
        i2=s.find('<div class="ad-detail-share-mobile linkblock visible-xs">')
        content=s[i:i2]
        content=cleanUp(content)
        return content
    except Exception as e:
        print (e)
        return str(e)
