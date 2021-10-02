import mysql.connector
import pandas as pd
import numpy as np
import json
import socket
import threading

pw='20040723caesar'
conect = mysql.connector.connect(user='root', password=pw, host='localhost', database='python1',auth_plugin='mysql_native_password')
running=True

def createDatabase():
    conect=mysql.connector.connect(user='root',password=pw,host='localhost')
    con=conect.cursor()
    con.execute('CREATE DATABASE python1')
def createTable():

    con = conect.cursor()
    con.execute('CREATE TABLE studentScore(ID int AUTO_INCREMENT PRIMARY KEY,Class VARCHAR(255),Name VARCHAR(255),Score int)')
def creatLogTable():

    con = conect.cursor()
    con.execute(
        'CREATE TABLE ScoreLog(ID int AUTO_INCREMENT PRIMARY KEY,Class VARCHAR(255),Name VARCHAR(255),Log VARCHAR(255),ScoreChange int)')
def addStudent(Class,name,score):

    con = conect.cursor()
    con.execute('INSERT INTO studentScore(Class,Name,Score) VALUES ("%s","%s",%s)'%(str(Class),str(name),score))
    conect.commit()
def addLog(Class,name,reason,Sc):

    con = conect.cursor()
    con.execute('INSERT INTO ScoreLog(Class,Name,Log,ScoreChange) VALUES ("%s","%s","%s",%s)'%(str(Class),str(name),str(reason),Sc))
    conect.commit()
def changeScore(Nam,num,reason):

    con = conect.cursor()
    con.execute('UPDATE studentScore SET Score=Score+%s WHERE Name="%s"'%(num,Nam))

    conect.commit()
    con.execute('SELECT Class ,Name,Score  FROM studentScore WHERE Name="%s"'%(Nam))
    get=con.fetchone()
    print(get)
    addLog(get[0],Nam,reason,num)
    return get[0]+' '+get[1]+' '+str(get[2])
def student():
    get=pd.read_excel('AllStudent.xlsx')
    print(getType(get['班级']))

    filt=Df2Lis(get[['班级','姓名']])
    for i in range(len(filt)):
        print(filt[i][0])
        addStudent(filt[i][0],filt[i][1],filt[i][2])
def checkStudent():

    name=[]
    cla=[]
    score=[]
    result=[]
    reason=[]
    con = conect.cursor()
    con.execute('SELECT Name,Class,Score FROM studentScore WHERE Score<85')
    students=con.fetchall()
    #print(students)
    for i in range(len(students)):
        reas=''
        print(students[i][0],students[i][1],students[i][2],end='      ')
        name.append(students[i][0])
        cla.append(students[i][1])
        score.append(students[i][2])

        con.execute('SELECT Log,ScoreChange FROM ScoreLog WHERE Name="%s"'%(students[i][0]))
        get=con.fetchall()
        for rea in get:
            #print(rea[0],rea[1],end=' | ')
            reas+=rea[0]+' '+str(rea[1])+' | '
        reason.append(reas)
        result.append(typePunishment(students[i][2]))
        print(typePunishment(students[i][2]))

    return [name,cla,score,result,reason]
def typePunishment(Score):
    s=int(Score)
    return '劝退' if s<50 else '留校察看' if s<60 else '记过处分' if s<70 else '书面警告' if s<80 else '口头警告'

def getType(series):
    arr=[]
    check=False
    for i in range(len(series)):
        for ii in arr:
            if series[i]==ii:
                check=True
        if check==False:
            arr.append(series[i])
        check=False
    return arr
def Df2Lis(data):
    if type(data)==list or type(data)==range or type(data)==np.ndarray:
        #print(list(data))
        return list(data)
    else:
        arr=[]
        arr2=[]
        for i in range(len(data[list(data)[0]])):
            arr2.append(data[list(data)[0]][i])
            arr2.append(data[list(data)[1]][i])
            arr2.append(100)
            arr.append(arr2)
            arr2=[]
        return arr
def getInfor():
    global running
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server :

        server.bind((socket.gethostname(), 8888))  # 8888是端口，客户端要一样
        server.listen(10)
        while running:
            print('Start')
            c, a = server.accept()
            #print((c.recv(1024).decode()))
            get = json.loads((c.recv(1024).decode()))
            print(len(get))
            if len(get)==1 and get[0]=='csv':
                check=checkStudent()
                c.send(json.dumps(check).encode())
            elif len(get)==3:
                print('r')
                try:
                    infor=[changeScore(get[0],get[1],get[2])]
                except:
                    infor=['名字错误']
                c.send(json.dumps(infor).encode())
        print('close')

thread=threading.Thread(target=getInfor)
thread.start()
while running:
    g=input('over? Y/N')
    if g=="Y":
        running=False
        print(running)