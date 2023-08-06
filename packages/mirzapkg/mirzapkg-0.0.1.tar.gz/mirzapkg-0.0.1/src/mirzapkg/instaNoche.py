#from instapy import InstaPy
from instabot import Bot
from random import randint
from time import sleep
from os import listdir
from os.path import isfile, join
import os
import glob


def UpLoad_dir(usr,passwrd,dirPath):

    cookie_del=glob.glob("config/*cookie.json")
    os.remove(cookie_del[0])
    bot=Bot()
    bot.login(username=usr,password=passwrd)
    ListOnlyFiles=[f for f in listdir(dirPath) if isfile(join(dirPath,f))]
    if len(ListOnlyFiles)>=11:
        print("illogical amount of photos for uploading")
        return 0
    else:
        for i in ListOnlyFiles:
            Npath=dirPath+'/'+i
            sleep(30)
            bot.upload_photo(Npath, caption=i)



def uploadOne(usr,passwrd,pathtophoto):
    cookie_del=glob.glob("config/*cookie.json")
    os.remove(cookie_del[0])
    bot=Bot()
    bot.login(username=usr,password=passwrd)
    sleep(30)
    bot.upload_photo(pathtophoto)
