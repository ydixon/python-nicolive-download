import requests, requests.utils, pickle
from requests import session
from xml.etree import ElementTree
import re
from cookielib import LWPCookieJar
import os
import sys

class NicoSession(object):

    LOGIN_URL = "https://secure.nicovideo.jp/secure/login?site=niconico"
    GETPLAYERSTATUS_URL = "http://live.nicovideo.jp/api/getplayerstatus?v="
    ACCOUNT_LIST_URL = "http://www.nicovideo.jp/my/mylist"
    COOKIE_NAME = "cookie"

    def __init__(self, mail_tel, password):
        self.mail_tel = mail_tel
        self.password = password

    def login(self, mail_tel=None, password=None):
        if mail_tel != None:
            self.mail_tel = mail_tel
        if password != None:
            self.password = password

        print self.mail_tel

        payload = {
            'mail_tel': self.mail_tel,
            'password': self.password
        }

    	cookie_path = self.getScriptPath() + "/" + self.COOKIE_NAME
    	self.session = self.loadSessionCookie(cookie_path)

        if not self.isLogin():
        	self.session = session()
        	login_result = self.session.post(self.LOGIN_URL, data=payload)
		self.saveSessionCookie(self.session, cookie_path)
        
	    #print(login_result.headers)

    def getStreamInfo(self, liveid):
        playerStatus = self.getPlayerStatus(self.session, liveid)
        title = playerStatus.find('stream/title').text
        provider_type = playerStatus.find('stream/provider_type').text
        rtmp_url = playerStatus.find('rtmp/url').text
        ticket = playerStatus.find('rtmp/ticket').text

        que_rtmp_list = []
        quesheet = playerStatus.find('stream/quesheet')
        ques = list(quesheet.iter("que"))
        for que in ques:
            que_rtmp = self.getQueRtmp(que.text, liveid);
            if que_rtmp != None:
                que_rtmp_list.append(que_rtmp)
        #print que_rtmp_list
        print "Found Video Segments: " + str(len(que_rtmp_list))
        info = { "liveid" : liveid,
                 "title" : title,
                 "provider_type": provider_type,
                 "rtmp_url" : rtmp_url,
                 "ticket" : ticket,
                 "que_rtmp_list" : que_rtmp_list
        }
        return info
    
    def saveSessionCookie(self, session, outputPath):
    	with open(outputPath, 'w') as f:
    	    pickle.dump(requests.utils.dict_from_cookiejar(session.cookies), f)

    def loadSessionCookie(self, inputPath):
    	if not os.path.exists('cookiejar'):
    		return None

    	with open(inputPath) as f:
        	cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
        	session = requests.session()
    		session.cookies = cookies
    	return session
	
    def isLogin(self):
        if self.session == None:
    	   return False
	    
        response = self.session.post(self.ACCOUNT_LIST_URL)
        if response.headers.get("x-niconico-authflag") == "1" or response.headers.get("x-niconico-authflag") == "3":
    		return True
    	else:
    		return False

    def getPlayerStatus(self, session, id):
        response = session.get("http://live.nicovideo.jp/api/getplayerstatus?v=" + id)
        #print (response.text)
        status = ElementTree.fromstring(response.content)
        if status.attrib["status"] != "ok":
            print "getplayerstatus failed"
        else:
            return status

    def getQueRtmp(self, que, liveid):
        matchObj = re.match("/publish " + liveid + " (.*)", que)
        if matchObj is None:
            return None
        return matchObj.group(1)

    def getScriptPath(self):
        return os.path.dirname(os.path.realpath(sys.argv[0]))

    
