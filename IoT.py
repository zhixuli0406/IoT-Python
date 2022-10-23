#coding: utf-8 
import urllib, json, time
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datafmt='%a, %d %b %Y %H:%M:%S',
    filename='./log/'+time.strftime("%Y-%m-%d", time.localtime())+'.log',
    filemode='a'
)
sched  = BackgroundScheduler()

def getSensor(url,name,layername,data) :
    response = urllib.urlopen(url.encode("utf-8"))
    jsonResponse = json.loads(response.read())
    data.extend(jsonResponse["value"])
    if  "@iot.nextLink" in jsonResponse: 
        return  getSensor(jsonResponse["@iot.nextLink"],name,layername,data)
    else :
        fn = layername + '.json'
        with open(fn,'w') as fnObj:
            json.dump(data,fnObj)        
        log = name + '[' + time.asctime(time.localtime(time.time())) + ']'
        print(log)
        return True
    
def AddThread():
    with open('./config.json') as f:
        jf = json.loads(f.read())
        print(u"\n-----更新開始[%s]-----"%time.asctime(time.localtime(time.time())))
        thread_list = []
        for sensor in jf["Sensor"]:
            data = []
            threadSensor = Thread(target=getSensor,args=(sensor["api"],sensor["name"],sensor["layername"],data))
            threadSensor.start()
            thread_list.append(threadSensor)
        for t in thread_list:
            t.join()
        print(u"-----更新結束[%s]-----\n"%time.asctime(time.localtime(time.time())))
        return True
trigger = IntervalTrigger(minutes=5)
sched.add_job(AddThread,trigger)
sched.start()
AddThread()
input()


    
