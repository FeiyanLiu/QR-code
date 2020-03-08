import os
import time
import sys
from PIL import Image
import qrcode
from pyzbar import pyzbar as pyzbar
from ffmpy3 import FFmpeg
import cv2
import numpy as np
import copy

def detect(image):

    width,height=image.shape[:2][::-1]
    img_gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    retval,binary=cv2.threshold(img_gray,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)
    contours,hierarchy=cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(img,contours,-1,(0,0,255),3)
    #cv2.imshow("img",img)
    #cv2.waitKey()
    return contours,hierarchy

def get_scale1(contours,i,j):
#外轮廓和子轮廓比例
    area1=cv2.contourArea(contours[i])
    area2=cv2.contourArea(contours[j])
    if area2==0:
        return False
    ratio = area1*1.0 / area2
    if abs(ratio-49.0/25):
        return True
    return False

def get_scale2(contours,i,j):
    #子轮廓和子子轮廓
    area1 = cv2.contourArea(contours[i])
    area2 = cv2.contourArea(contours[j])
    if area2 == 0:
        return False
    ratio = area1 * 1.0 / area2
    if abs(ratio - 25.0 / 9):
        return True
    return False

def get_center(contours,i,):
    M=cv2.moments(contours[i])
    cx=int(M['m10']/M['m00'])
    cy=int(M['m01']/M['m00'])
    return cx,cy

def detect_contours(vec):
    distance_1=np.sqrt((vec[0]-vec[2])**2+(vec[1]-vec[3])**2)
    distance_2 = np.sqrt((vec[0] - vec[4]) ** 2 + (vec[1] - vec[5]) ** 2)
    distance_3 = np.sqrt((vec[2] - vec[4]) ** 2 + (vec[3] - vec[5]) ** 2)
    if sum((distance_1,distance_2,distance_3))/3<3:
        return True
    return False

def triangle(rec):
    if len(rec) < 3:
        return -1, -1, -1
    for i in range(len(rec)):
        for j in range(i + 1, len(rec)):
            for k in range(j + 1, len(rec)):
                distance_1 = np.sqrt((rec[i][0] - rec[j][0]) ** 2 + (rec[i][1] - rec[j][1]) ** 2)
                distance_2 = np.sqrt((rec[i][0] - rec[k][0]) ** 2 + (rec[i][1] - rec[k][1]) ** 2)
                distance_3 = np.sqrt((rec[j][0] - rec[k][0]) ** 2 + (rec[j][1] - rec[k][1]) ** 2)
                if abs(distance_1 - distance_2) < 5:
                    if abs(np.sqrt(np.square(distance_1) + np.square(distance_2)) - distance_3) < 5:
                        return i, j, k
                elif abs(distance_1 - distance_3) < 5:
                    if abs(np.sqrt(np.square(distance_1) + np.square(distance_3)) - distance_2) < 5:
                        return i, j, k
                elif abs(distance_2 - distance_3) < 5:
                    if abs(np.sqrt(np.square(distance_2) + np.square(distance_3)) - distance_1) < 5:
                        return i, j, k
    return -1, -1, -1

def find(image,contours,hierachy,root=0):
    rec=[]
    for i in range(len(hierachy)):
        child = hierachy[i][2]
        child_child=hierachy[child][2]
        if child!=-1 and hierachy[child][2]!=-1:
            if get_scale1(contours,i,child) and get_scale2(contours,child,child_child):
                cx1,cy1=get_center(contours,i)
                cx2,cy2=get_center(contours,child)
                cx3,cy3=get_center(contours,child_child)
                if detect_contours([cx1,cy1,cx2,cy2,cx3,cy3]):
                    rec.append([cx1,cy1,cx2,cy2,cx3,cy3,i,child,child_child])
    i,j,k=triangle(rec)
    if i==-1 or j==-1 or k==-1:
        return
    ts=np.concatenate((contours[rec[i][6]],contours[rec[j][6]],contours[rec[k][6]]))
    rect=cv2.minAreaRect(ts)
    box=cv2.boxPoints(rect)
    box=np.int0(box)
    result= copy.deepcopy(image)
    #cv2.drawContours(result, [box], 0, (0, 0, 255), 2)
    #cv2.drawContours(image, contours, rec[i][6], (255, 0, 0), 2)
    #cv2.drawContours(image, contours, rec[j][6], (255, 0, 0), 2)
    #cv2.drawContours(image, contours, rec[k][6], (255, 0, 0), 2)
    cv2.imshow('img', image)
    cv2.waitKey(0)
    cv2.imshow('img', result)
    cv2.waitKey(0)
    new_image = copy.deepcopy(image)
    min=box[0][0]
    max=box[0][0]

    leftup=box[1][1]
    rightup=box[0][1]
    leftbuttom=box[0][0]
    rightbuttom=box[2][0]
    new_image=image[leftup:rightup,leftbuttom:rightbuttom]
    cv2.imshow('img', new_image)
    cv2.waitKey(0)
    new_image1=cv2.resize(new_image,(512,512))
    cv2.imshow('img', new_image1)
    cv2.waitKey(0)
    return





if __name__ == "__main__":
    #img_path=r'G:/project1outpic/1.jpg'
    img_path = r'G:/project1outpic/1.png'
    img_path = r'G:/test2.jpg'
    #img_path = r'G:/test1.jpg'
    img=cv2.imread(img_path)
    contours,hierachy=detect(img)
    find(img,contours,np.squeeze(hierachy))