# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 21:42:03 2018

@author: Sourav
"""
import os
import cv2
import time
import numpy as np
import pyttsx3 as t2s   #text to speech
import wx 
import socket
#%%
UDP_IP = '192.168.4.1'
UDP_PORT = 80
BUFFER_SIZE = 1024
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    del app
except:
    pass

def nop(x):
    pass

os.system('clear');  #clearing the python console
#sp.call("E://GMIT//EyeGaze//WebGazer-master//www//START.bat",shell=True)
app=wx.App(False)
(sx,sy)=wx.GetDisplaySize()
cap=cv2.VideoCapture('http://192.168.4.3:8080/video')

#text to speech initilization
eng=t2s.init()


def text2speech(text):
    try:
        eng.setProperty('rate',120);eng.setProperty('volume',.9)
        eng.say(text)
        eng.runAndWait()
    except:
        pass

st=time.time()

while(1):
    _,img=cap.read();
#    img=cv2.flip(img,2)
#    frame=np.ones((sy,sx,3),dtype='uint8')*255
    frame=cv2.resize(img,(sx,sy))
    try:
        for line in open("C://Users//Sourav//AppData//Local//Google//Chrome//User Data//chrome_debug.log"):
            last=line
        ax=last.find('x')
        ay=last.find('y')
    except:
        break;
    if ax<0 or ay<0:
        continue
    cord=last[ax+3:ax+8]+" "+last[ay+3:ay+8];
    
    temp=''
    for w in cord:
        if str.isdigit(w):
            temp+=w
        else:
            temp+=' '
    A=np.abs([int(s) for s in temp.split() if s.isdigit()])
    
    if np.any(A):
        #%%#  0-stop,1-Left,2-Right,3-Forward,4-Backward
        loc=-1
        try:
            if A[0]>(sx//3)-140 and A[0]<(2*sx//3)+140:
                if A[1]<(sy//3)-40:
                    x=(sx//2)
                    y=(sy//6)-20
                    text="Foward"
                    loc=3
                elif A[1]<(2*sy//3)+40:
                    x=(sx//2)
                    y=(sy//2)
                    text="Stop"
                    loc=0
                elif A[1]<sy:
                    x=(sx//2)
                    y=(5*sy//6)+20
                    text="Backward"
                    loc=4
            elif A[0]<((sx//3)-140):
                x=(sx//6)-70
                y=(sy//2)
                Xa=0;Ya=(sy//3);Xb=(sx//3);Yb=(2*sy//3)
                text="Left"
                loc=1
            elif A[0]>(2*sx//3)+140:
                x=(5*sx//6)+70
                y=(sy//2)
                Xa=(2*sx//3);Ya=(sy//3);Xb=(sx);Yb=(2*sy//3)
                text="Right"
                loc=2
            print(text)
            MESSAGE = '%'+str(loc)+'\r\n'
#           print(MESSAGE)
            try:
                s.sendto(MESSAGE.encode(),(UDP_IP, UDP_PORT))
            except:
                break
        except:
            continue
        
            
        #%%
        
#        try:
#            t=threading.Thread(name='child',target=text2speech,args=('hello',))
#            if not t.is_alive():
#                t.start()
#        except:
#            pass
#        try:
#            frame[Ya:Yb,Xa:Xb]=img[Ya:Yb,Xa:Xb];
#        except:
#            pass
     #%%   
    frame=cv2.line(frame,((sx//3)-140,(sy//3)-40),(2*(sx//3)+140,(sy//3)-40),(250,0,0),2)
    frame=cv2.line(frame,((sx//3)-140,0),((sx//3)-140,sy),(250,0,0),2)
    frame=cv2.line(frame,(((2*sx)//3)+140,0),((2*sx//3)+140,sy),(250,0,0),2)
    frame=cv2.line(frame,((sx//3)-140,(2*sy//3)+40),(2*sx//3+140,(2*sy//3)+40),(250,0,0),2)
        
    cv2.putText(frame,'Forward',((sx//2)-120,(sy//6)+30), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,255,255),3,cv2.LINE_AA)
    cv2.putText(frame,'Left',((sx//6)-140,(sy//2)+30), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,255,255),3,cv2.LINE_AA)
    cv2.putText(frame,'Stop',((sx//2)-80,(sy//2)+30), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,255,255),3,cv2.LINE_AA)
    cv2.putText(frame,'Right',((5*sx//6)-10,(sy//2)+30), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,255,255),3,cv2.LINE_AA)
    cv2.putText(frame,'Backward',((sx//2)-150,(5*sy//6)+30), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,255,255),3,cv2.LINE_AA)
   
    
    frame=cv2.circle(frame,(x,y),10,(0,255,0),-1);
    frame=cv2.circle(frame,(x,y),17,(255,0,0),2);
    
#    img=cv2.resize(img,(Xb-Xa,Yb-Ya)) ;
#    frame[Ya:Yb,Xa:Xb]=img;

    cv2.imshow('Canvas',frame)
    if cv2.waitKey(1)==27:
        break
#        mouse.move(A[0],A[1],absolute=True, duration=.1)
#%%
MESSAGE='%0\r\n'
try:
    s.sendto(MESSAGE.encode(),(UDP_IP, UDP_PORT))
except:
    pass
cv2.destroyAllWindows()
cap.release()