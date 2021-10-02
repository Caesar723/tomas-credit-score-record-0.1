import socket
from tkinter import*
import json
import pandas as pd
import os
hostN = '192.168.2.14'
path='/Users/chenxuanpei/Desktop/修改'
def getchange():
    postNum = 8888
    get=os.listdir(path)
    print(get)
    for i in get:
        ge=pd.read_excel(path+'/'+i)
        name=(ge.columns)
        #print(ge[name[0]])
        for ii in range(len(ge[name[0]])):
            #print([ge.iloc[ii][name[0]], ge.iloc[ii][name[1]], ge.iloc[ii][name[2]]])
            door = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            door.connect((hostN, postNum))
            door.send(json.dumps([ge.iloc[ii][name[0]], int(ge.iloc[ii][name[1]]), ge.iloc[ii][name[2]]]).encode())
            get = json.loads((door.recv(1024).decode()))
            love.config(text=get[0])
            print(get[0],ge.iloc[ii][name[0]],(int(ge.iloc[ii][name[1]]), ge.iloc[ii][name[2]]) if get[0]=='名字错误' else '')
        os.remove(path+'/'+i)
def ok():

    postNum = 8888
    door = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    door.connect((hostN, postNum))
    door.send(json.dumps([em1.get(),int(em2.get()),em3.get()]).encode())
    get = json.loads((door.recv(1024).decode()))

    if len(get) == 1:
        love.config(text=get[0])
    else:
        df = pd.DataFrame({
            "姓名": get[0],
            "班级": get[1],
            "积分": get[2],
            "措施": get[3],
            "日志": get[4]
        })
        df.to_csv("问题学生.csv", index=False)
    door.close()
def checkStudent():

    postNum = 8888
    door = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    door.connect((hostN, postNum))
    door.send(json.dumps(['csv']).encode())
    get = json.loads((door.recv(1024).decode()))
    print(get)
    if len(get) == 1:
        love.config(text=get[0])
    else:
        df = pd.DataFrame({
            "姓名": get[0],
            "班级": get[1],
            "积分": get[2],
            "措施": get[3],
            "日志": get[4]
        })
        df.to_csv("问题学生.csv", index=False)
    door.close()
def getInfo():
    print('ok')
    postNum = 8888
    door = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    door.connect((hostN, postNum))
    while True:
        get = json.loads(json.dumps(door.recv(1024).decode()))
        print(get)
        if len(get)==1:
            love.config(text=get[0])
        else:
            df = pd.DataFrame({
                "姓名": get[0],
                "班级": get[1],
                "积分": get[2],
                "措施": get[3],
                "日志": get[4]
            })
            df.to_csv("问题学生.csv", index=False)

window=Tk()
window.title("Tomas Student SQL")
window.geometry("600x600+500+200")

love=Label(window,width=20,text="对学生进行加减分")
love.place(x=40,y=30)

name=Label(window,width=5,text="名字")
name.place(x=10,y=60)
score=Label(window,width=10,text="分数变化")
score.place(x=70,y=60)
reason=Label(window,width=5,text="原因")
reason.place(x=190,y=60)
em1=Entry(window,width=5)
em1.place(x=10,y=100)
em2=Entry(window,width=5)
em2.place(x=90,y=100)
em3=Entry(window,width=10)
em3.place(x=190,y=100)
yes=Button(window,text="确认",width=10,command=ok)
yes.place(x=80,y=150)
no=Button(window,text="检查SQL并生成表格文件",width=20,command=checkStudent)
no.place(x=40,y=290)
n=Button(window,text="将文件里的xlsx文件里记录提取出来",width=30,command=getchange)
n.place(x=280,y=290)
window.mainloop()