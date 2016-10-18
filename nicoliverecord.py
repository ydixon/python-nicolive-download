#!/usr/bin/python
import os
import subprocess
import sys, getopt
import re
import collections
from urlparse import urlparse

from NicoSession import NicoSession

python_script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
rtmp_path =  python_script_path + "/rtmpdump-ksv-nicolive/rtmpdump"
mail_tel = "" #set login name
password = "" #set password

def getScriptPath():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def getValidFileName(filename):
   #replace backslashes with "-"
   filename = re.sub(r"\/", "-", filename)
   return filename

def getLiveid(url):
   if url.startswith("lv"):
      return url
   else:
      o = urlparse(url)
      url_without_query_string = o.scheme + "://" + o.netloc + o.path
      liveid = url_without_query_string.rsplit("/")[-1]
      return liveid

def runRTMP(rtmp_path, args, isSync):
   shellcmd = rtmp_path
   for arg in args:
      if arg and not arg.isspace():
         shellcmd+= " " + arg
   print shellcmd      
   task = subprocess.Popen(shellcmd, shell=True)
   if (isSync):
      task.wait()

def downloadChannelStream(rtmp_path, info):
    for k, que_rtmp in enumerate(info['que_rtmp_list']):
        filename = '"{}"'.format(info['title'].encode('utf-8') + "_" + info['liveid'] + "_" + str(k) + ".flv")
        cmd =  "%s -o %s -r %s -y %s -C %s" % ( rtmp_path,
                                                getValidFileName(filename),
                                                '"{}"'.format(info['rtmp_url']),
                                                "mp4:/" + que_rtmp,
                                                "S:" + '"{}"'.format(info['ticket']))
        print cmd
        task = subprocess.Popen(cmd, shell=True)
        task.wait()

def downloadCommunityStream(rtmp_path, info):
    for k, que_rtmp in enumerate(info['que_rtmp_list']):
        filename = '"{}"'.format(info['title'].encode('utf-8') + "_" + info['liveid'] + "_" + str(k) + ".flv")
        cmd =  "%s -o %s -vr %s -C %s -N %s" % ( rtmp_path,
                                                 getValidFileName(filename),
                                                 '"{}"'.format(info['rtmp_url']),
                                                 "S:" + '"{}"'.format(info['ticket']),
                                                 '"{}"'.format(que_rtmp))
        print cmd
        task = subprocess.Popen(cmd, shell=True)
        task.wait()

def downloadStream(rtmp_path, info):
    provider_type = info['provider_type']
    if (provider_type == "channel"):
        downloadChannelStream(rtmp_path, info)
    elif (provider_type == "community"):
        downloadCommunityStream(rtmp_path, info)
   
def main(argv):
   print python_script_path 
   inputfile = ''
   outputfile = ''   #doesn't do anything yet
   try:
      opts, args = getopt.getopt(argv,"hl:o:",["liveid=","ofile="])
   except getopt.GetoptError:
      print 'test.py -l <liveid> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'nicoliverecord.py -l <liveid> -o <outputfile>'
         sys.exit()
      elif opt in ("-l", "--liveid"):
         inputid = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   
   liveid =  getLiveid(inputid)
   print "Downloading " + liveid
   
   nicoSession = NicoSession(mail_tel, password)
   nicoSession.login()
   info = nicoSession.getStreamInfo(liveid)
   downloadStream(rtmp_path, info)
   #print info

if __name__ == "__main__":
   main(sys.argv[1:])
