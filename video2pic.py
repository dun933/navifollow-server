# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 16:23:07 2019

@author: vesper
"""
import os
import cv2
# 使用opencv按一定间隔截取视频帧，并保存为图片
vc = cv2.VideoCapture('d:/test2.mp4') #读取视频文件
c = 1
rval=True 
# if vc.isOpened():#判断是否正常打开
#     rval,frame = vc.read()
# else:
#     rval = False
timeF = 21 #视频帧计数间隔频率
while rval: #循环读取视频帧
    rval,frame = vc.read()
    if(c%timeF==0):
        cv2.imwrite('d:/video_pics/'+str(c)+'.jpg',frame) # 存储为图像
    c = c + 1
    cv2.waitKey(1)
vc.release()
if __name__=="__main__":
    os.system("python wwhtest.py")   
