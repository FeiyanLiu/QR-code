import os
import time
import sys
from ffmpy3 import FFmpeg
import os
import time
import sys
from ffmpy3 import FFmpeg
import cv2
import numpy as np
import copy




'''检测轮廓'''
def detect(image):

    width,height=image.shape[:2][::-1]
    img_gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)#转灰度图
    retval,binary=cv2.threshold(img_gray,100,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)#二值化处理
    contours,hierarchy=cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#等级树结构轮廓
    #cv2.drawContours(img,contours,-1,(0,0,255),3)
    #cv2.imshow("img",image)
    #cv2.waitKey()
    return contours,hierarchy
'''
轮廓比例 边占比7：5
'''
def get_scale1(contours,i,j):
#外轮廓和子轮廓比例 1:1：3：1:1
    area1=cv2.contourArea(contours[i])#轮廓面积1
    area2=cv2.contourArea(contours[j])#轮廓面积2
    if area2==0:#无子轮廓
        return False
    ratio = area1*1.0 / area2
    if abs(ratio-49.0/25): # 7/5
        return True
    return False
'''轮廓比例 边占比5：3'''
def get_scale2(contours,i,j):
    #子轮廓和子子轮廓
    area1 = cv2.contourArea(contours[i])#轮廓面积1
    area2 = cv2.contourArea(contours[j])#轮廓面积2
    if area2 == 0:#无子轮廓
        return False
    ratio = area1 * 1.0 / area2
    if abs(ratio - 25.0 / 9):# 5/3
        return True
    return False
'''
求轮廓中心坐标
'''
def get_center(contours,i):
    M=cv2.moments(contours[i]) #求矩阵
    cx=int(M['m10']/M['m00']) #求x坐标
    cy=int(M['m01']/M['m00']) #求y坐标
    return cx,cy
'''判断中心间距'''
def detect_contours(vec):
    distance_1=np.sqrt((vec[0]-vec[2])**2+(vec[1]-vec[3])**2)#1、2两点的距离
    distance_2 = np.sqrt((vec[0] - vec[4]) ** 2 + (vec[1] - vec[5]) ** 2)#1、3两点的距离
    distance_3 = np.sqrt((vec[2] - vec[4]) ** 2 + (vec[3] - vec[5]) ** 2)#2、3两点的距离
    if sum((distance_1,distance_2,distance_3))/3<3:
        return True
    return False

def triangle(rec):#是否组成三角形
    if len(rec) < 3:
        return -1, -1, -1
    '''判断边长是否满足三角形条件'''
    for i in range(len(rec)):
        for j in range(i + 1, len(rec)):
            for k in range(j + 1, len(rec)):
                distance_1 = np.sqrt((rec[i][0] - rec[j][0]) ** 2 + (rec[i][1] - rec[j][1]) ** 2)
                distance_2 = np.sqrt((rec[i][0] - rec[k][0]) ** 2 + (rec[i][1] - rec[k][1]) ** 2)
                distance_3 = np.sqrt((rec[j][0] - rec[k][0]) ** 2 + (rec[j][1] - rec[k][1]) ** 2)
                if abs(distance_1 - distance_2) < 6:
                    if abs(np.sqrt(np.square(distance_1) + np.square(distance_2)) - distance_3) < 6:
                        return i, j, k
                elif abs(distance_1 - distance_3) < 6:
                    if abs(np.sqrt(np.square(distance_1) + np.square(distance_3)) - distance_2) < 6:
                        return i, j, k
                elif abs(distance_2 - distance_3) < 6:
                    if abs(np.sqrt(np.square(distance_2) + np.square(distance_3)) - distance_1) < 6:
                        return i, j, k
    return -1, -1, -1
'''
用于寻找轮廓
hierarchy[][i]，i 0-3 分别后一个轮廓的序号、前一个轮廓的序号、子轮廓的序号、父轮廓的序号
'''
def find(image,contours,hierachy,root=0):#寻找轮廓
    rec=[]
    for i in range(len(hierachy)):
        child = hierachy[i][2]#得到子轮廓
        child_child=hierachy[child][2]#得到子子轮廓
        if child!=-1 and hierachy[child][2]!=-1:#两种轮廓都存在
            if get_scale1(contours,i,child) and get_scale2(contours,child,child_child):
                cx1,cy1=get_center(contours,i)#父轮廓中心
                cx2,cy2=get_center(contours,child)#子轮廓中心
                cx3,cy3=get_center(contours,child_child)#子子轮廓中心
                if detect_contours([cx1,cy1,cx2,cy2,cx3,cy3]):
                    rec.append([cx1,cy1,cx2,cy2,cx3,cy3,i,child,child_child])
    i,j,k=triangle(rec)
    '''不能成三角形，结束函数'''
    if i==-1 or j==-1 or k==-1:
        return
    ts=np.concatenate((contours[rec[i][6]],contours[rec[j][6]],contours[rec[k][6]]))#矩阵拼接
    rect=cv2.minAreaRect(ts)#最小外接矩形
    box=cv2.boxPoints(rect)#矩形边缘
    box=np.int0(box)
    #result= copy.deepcopy(image)
    #cv2.drawContours(result, [box], 0, (0, 0, 255), 2)
    #cv2.drawContours(image, contours, rec[i][6], (255, 0, 0), 2)
    #cv2.drawContours(image, contours, rec[j][6], (255, 0, 0), 2)
    #cv2.drawContours(image, contours, rec[k][6], (255, 0, 0), 2)
    #cv2.imshow('img', image)
    #cv2.waitKey(0)
    #cv2.imshow('img', result)
    cv2.waitKey(0)
    #new_image = copy.deepcopy(image)#复制备份


    #leftup=box[1][1]
    #rightup=box[0][1]
    #leftbuttom=box[0][0]
    #rightbuttom=box[2][0]
    '''
    测试出的位置
    '''
    leftup = box[2][1]
    rightup = box[0][1]
    leftbuttom = box[1][0]
    rightbuttom = box[3][0]

    '''
    裁剪图片
    '''
    new_image=image[leftup:rightup,leftbuttom:rightbuttom]
    #new_image=image[43:1025,403:1387]
    #cv2.imshow('img', new_image)
    #cv2.waitKey(0)
    new_image1=cv2.resize(new_image,(1000,1000))
    #cv2.imshow('img', new_image1)
    cv2.waitKey(0)
    return new_image1

def bintostr(s):
    count = 0
    sum = 0
    outStr = ''
    for i in s:
        temp = (ord(i)-ord("0")) * pow(2, 7 - count)
        sum += temp
        count += 1
        if (count == 8):
            count = 0

            if(sum==255):
                return outStr
            outStr = outStr + (chr(sum))
            sum = 0

    #print(outStr)
    return outStr


#
if __name__ == "__main__":

    #img_path = r'G:/project1pic/1.png'
    #img_path = r'G:/test1.jpg'
    img_path = r'G:/testpic/test9.jpg'
    img_path = r'G:/testpic/test1.png'
    #img_path = r'G:/test.png'
    img_path=r'G:/project1outpic/7.png'
    img = cv2.imread(img_path)
    #contours,hierachy=detect(img)
    #find(img,contours,np.squeeze(hierachy))
    #decode(img)
    # img_path = r'G:/testpic/test14.jpg'
    # img=cv2.imread(img_path)
    # decode(img)