import os
import time
import sys
from PIL import Image
import qrcode
from pyzbar import pyzbar as pyzbar
from ffmpy3 import FFmpeg
import cv2
import numpy as np
import glob as gb
import locate


def str2bin(s):
    temp=[]
    for c in s:
        temp.append(bin(c).replace('0b',''))
    str_bin=' '.join(temp)
    return str_bin
# def newQrcode():#初始化二维码（一个一个打出来的，三个定位点
#     img = np.ones((512, 512), dtype=np.uint8)
#     img[0:128, 0:128] = 255
#     img[0:112, 0:112] = 0
#     img[16:80, 16:80] = 255
#     img[32:64, 32:64] = 0
#
#     img[384:512, 0:128] = 255
#     img[400:512, 0:112] = 0
#     img[432:496, 16:80] = 255
#     img[448:480, 32:64] = 0
#
#
#     img[0:128, 384:512] = 255
#     img[0:112, 400:512] = 0
#     img[16:80, 432:496] = 255
#     img[32:64, 448:480] = 0
#     return img

def newQrcode(size, lpsize):  # 初始化二维码（一个一个打出来的，三个定位点

    # location point size定位点尺寸
    # print((lpsize*6)/7)
    # 用参数表示每个边的坐标
    size = 1000  # 图片尺寸
    cube = 20  # 每个单元的大小
    lpsize = 200  # 定位点尺寸 8的倍数
    rate = 2
    img = np.ones((size, size*rate,3), dtype=np.uint8)
    img[0:int(lpsize), 0:int(lpsize)] = 255
    img[0:int(lpsize * 7 / 8), 0:int(lpsize * 7 / 8)] = 0
    img[int(lpsize / 8):int(lpsize * 6 / 8), int(lpsize / 8):int(lpsize * 6 / 8)] = 255
    img[int(lpsize * 2 / 8):int(lpsize * 5 / 8), int(lpsize * 2 / 8):int(lpsize * 5 / 8)] = 0
    # 左上角
    img[size - int(lpsize):size, 0:int(lpsize)] = 255
    img[size - int(lpsize * 7 / 8):size, 0:int(lpsize * 7 / 8)] = 0
    img[size - int(lpsize * 6 / 8):size - int(lpsize / 8), int(lpsize / 8):int(lpsize * 6 / 8)] = 255
    img[size - int(lpsize * 5 / 8):size - int(lpsize * 2 / 8), int(lpsize * 2 / 8):int(lpsize * 5 / 8)] = 0
    # 左下角

    img[0:int(lpsize), size*rate - int(lpsize):size*rate] = 255
    img[0:int(lpsize * 7 / 8), size*rate - int(lpsize * 7 / 8):size*rate] = 0
    img[int(lpsize / 8):int(lpsize * 6 / 8), size*rate - int(lpsize * 6 / 8):size*rate - int(lpsize / 8)] = 255
    img[int(lpsize * 2 / 8):int(lpsize * 5 / 8), size*rate - int(lpsize * 5 / 8):size*rate - int(lpsize * 2 / 8)] = 0
    # 右上角
    return img

def newQrcodewhite(size, lpsize):  # 初始化二维码（一个一个打出来的，三个定位点

    # location point size定位点尺寸
    # print((lpsize*6)/7)
    # 用参数表示每个边的坐标
    size = 1000  # 图片尺寸
    cube = 20 # 每个单元的大小
    lpsize = 200 # 定位点尺寸 8的倍数
    rate = 2
    img = np.ones((size, size*rate,3), dtype=np.uint8)
    img[0:size,0:size*rate]=255
    img[0:int(lpsize), 0:int(lpsize)] = 255
    img[0:int(lpsize * 7 / 8), 0:int(lpsize * 7 / 8)] = 0
    img[int(lpsize / 8):int(lpsize * 6 / 8), int(lpsize / 8):int(lpsize * 6 / 8)] = 255
    img[int(lpsize * 2 / 8):int(lpsize * 5 / 8), int(lpsize * 2 / 8):int(lpsize * 5 / 8)] = 0
    # 左上角
    img[size - int(lpsize):size, 0:int(lpsize)] = 255
    img[size - int(lpsize * 7 / 8):size, 0:int(lpsize * 7 / 8)] = 0
    img[size - int(lpsize * 6 / 8):size - int(lpsize / 8), int(lpsize / 8):int(lpsize * 6 / 8)] = 255
    img[size - int(lpsize * 5 / 8):size - int(lpsize * 2 / 8), int(lpsize * 2 / 8):int(lpsize * 5 / 8)] = 0
    # 左下角

    img[0:int(lpsize), size*rate - int(lpsize):size*rate] = 255
    img[0:int(lpsize * 7 / 8), size*rate - int(lpsize * 7 / 8):size*rate] = 0
    img[int(lpsize / 8):int(lpsize * 6 / 8), size*rate - int(lpsize * 6 / 8):size*rate - int(lpsize / 8)] = 255
    img[int(lpsize * 2 / 8):int(lpsize * 5 / 8), size*rate - int(lpsize * 5 / 8):size*rate - int(lpsize * 2 / 8)] = 0
    # 右上角
    return img

def odd_en(b):
    odd=0
    for i in range(7):
        if b[i]=='0':
            odd+=1
    if odd%2==1:
        b+='0'
    else: b+='1'
    return b

def encode_start():
    size = 1000  # 图片尺寸
    cube = 20  # 每个单元的大小
    lpsize = 200  # 定位点尺寸 8的倍数
    countx = 0
    county = lpsize
    rate =2
    QR_number = 2
    QR_print_number = 0
    img = newQrcodewhite(size, lpsize)
    img=combine_QR_code(img)
    cv2.imwrite(r'G:/project1pic/' + '1.png', img)
    img = newQrcode(size, lpsize)
    img = combine_QR_code(img)
    cv2.imwrite(r'G:/project1pic/' + '2.png', img)


def encode():
    file = open(r'G:/project1txt/test1.txt', 'rb')
    str1 = file.read()
    print(str1)
    str2 = str2bin(str1)
    size = 1000  # 图片尺寸
    cube = 20  # 每个单元的大小
    lpsize = 200  # 定位点尺寸 8的倍数
    countx = 0
    rate = 2
    county = lpsize
    QR_number = 3
    QR_print_number = 0
    encode_start()
    img = newQrcode(size, lpsize)
    B, G, R = cv2.split(img)
    colorstate = 0


    for c in str1:
        b = bin(c).replace('0b', '')
        b = b.rjust(7, '0')
        b=odd_en(b)
        for b1 in b:
            if countx == size:
                if colorstate==0:
                    QR_number += 1
                county = lpsize
                countx = 0
            if b1 == '0':
                img[countx:countx + cube, county:county + cube,colorstate] = 255  # 16*16的小方格视为为一个单位
            else:
                img[countx:countx + cube, county:county + cube,colorstate] = 0  # 0白1黑
            county += cube
            # 按照区域对于county如何变化分类讨论
            if county == size*rate - lpsize and countx < lpsize - cube:
                county = lpsize
                countx += cube  # 到达下一行
            elif county == size*rate - lpsize and countx == lpsize - cube:
                county = 0
                countx += cube
            elif county == size*rate and countx < size - lpsize - cube:
                county = 0
                countx += cube
            elif county == size*rate and countx == size - lpsize - cube:
                county = lpsize
                countx += cube
            elif county == size*rate and countx >= size - lpsize:
                county = lpsize
                countx += cube
            if countx == size and county == lpsize:
                if colorstate==2:
                    img=combine_QR_code(img)
                    cv2.imwrite(r'G:/project1pic/' + str(QR_number) + '.png', img)
                    QR_print_number += 1
                    img = newQrcode(1000, 200)
                    colorstate=0
                else: colorstate+=1
    if QR_print_number < QR_number:  # 判断此时是否需要再将图片打印出来
        img = combine_QR_code(img)
        cv2.imwrite(r'G:/project1pic/' + str(QR_number) + '.png', img)


def combine_QR_code(img):
    size = 1000  # 图片尺寸
    cube = 20  # 每个单元的大小
    lpsize =200  # 定位点尺寸 8的倍数
    #img=cv2.imread(img_path)
    background=np.ones((size+40,size*rate+40),dtype=np.uint8)*255
    background=cv2.cvtColor(background,cv2.COLOR_GRAY2BGR)
    #img=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    for i in range(20, 1020):
        for j in range(20, 2020):
            background[i, j, 0] = img[i - 20, j - 20, 0]
            background[i, j, 1] = img[i - 20, j - 20, 1]
            background[i, j, 2] = img[i - 20, j - 20, 2]
    return background
    #cv2.imshow("last",background)
    #cv2.waitKey()



def decode_start(img):
    if(type(img)==type(None)):
        return False
    size = 1000
    rate = 2
    lpsize = 200+20
    cube = 20
    countx = 0
    county = lpsize
    while countx < size:
        #print(np.sum(img[countx:countx + cube, county:county + cube]))
        if np.sum(img[countx:countx + cube, county:county + cube]) > 150000:  # 这里相当于是取小像素块的平均值，考虑到后面手机拍摄可能会产生色差
            return False
        county += cube
        # 这一块的分类讨论和encode是一样的
        if county == size*rate - lpsize and countx < lpsize - cube:
            county = lpsize
            countx += cube  # 到达下一行
        elif county == size*rate - lpsize and countx == lpsize - cube:
            county = 0
            countx += cube
        elif county == size*rate and countx < size - lpsize - cube:
            county = 0
            countx += cube
        elif county == size*rate and countx == size - lpsize - cube:
            county = lpsize
            countx += cube
        elif county == size*rate and countx >= size - lpsize:
            county = lpsize
            countx += cube
    if countx == size and county == lpsize:
        return True

def decode():
    #cv2.imshow("img",img)
    pic_number = 1
    size = 1000
    lpsize = 200
    cube = 20
    countx = 0
    county = lpsize
    bin1 = ''
    bin_number = 0
    str1 = ""
    colorstate=0
    count=101
    rate = 2

    img = cv2.imread(r'G:/project1outpic/1.png')
    if(type(img)==type(None)):
        return
    contours, hierachy = locate.detect(img)
    img=locate.find(img, contours, np.squeeze(hierachy))
    #cv2.imshow("2",img)
    while(not decode_start(img)):
        pic_number+=1
        #print(pic_number)
        img = cv2.imread(r'G:/project1outpic/' + str(pic_number) + '.png')
        if(type(img) == type(None)):
            #print("no")
            return
        contours, hierachy = locate.detect(img)
        img = locate.find(img, contours, np.squeeze(hierachy))
        while (type(img) == type(None)):
            print("未检测到定位点")
            pic_number+=1
            img = cv2.imread(r'G:/project1outpic/' + str(pic_number) + '.png')
            if (type(img) == type(None)):
                return
            contours, hierachy = locate.detect(img)
            img = locate.find(img, contours, np.squeeze(hierachy))
        #decode_start(img)
    pic_number+=1
    #print(pic_number)

    #pic_number=3
    img  = cv2.imread(r'G:/project1outpic/' + str(pic_number) + '.png')
    if (type(img) == type(None)):
        return
    #cv2.imshow("img",img)
    contours, hierachy = locate.detect(img)
    img = locate.find(img, contours, np.squeeze(hierachy))
    if (type(img) == type(None)):
        print("未检测到定位点")

    #print(pic_number)
    while colorstate<2:
        count+=1

        while countx < size:
            #print(type(img))
            #print(colorstate)
            #print(np.sum(img[countx:countx + cube, county:county + cube,colorstate]))
            if np.sum(img[countx:countx + cube, county:county + cube,colorstate]) < 54000:  # 这里相当于是取小像素块的平均值，考虑到后面手机拍摄可能会产生色差
                bin1 = bin1 + '1'
            else:
                bin1 = bin1 + '0'
            #print(bin1)
            county += cube
            # 这一块的分类讨论和encode是一样的
            if county == size*rate - lpsize and countx < lpsize - cube:
                county = lpsize
                countx += cube  # 到达下一行
            elif county == size*rate - lpsize and countx == lpsize - cube:
                county = 0
                countx += cube
            elif county == size*rate and countx < size - lpsize - cube:
                county = 0
                countx += cube
            elif county == size*rate and countx == size - lpsize - cube:
                county = lpsize
                countx += cube
            elif county == size*rate and countx >= size - lpsize:
                county = lpsize
                countx += cube

            if countx == size and county == lpsize:
                colorstate+=1
                #print(colorstate)
                if colorstate==3:
                    colorstate=0
                    pic_number += 1
                    #countx = 520
                    #print(pic_number)
                    img = cv2.imread(r'G:/project1outpic/' + str(
                        pic_number) + '.png')  # 这一段可读性太差，意思是取完全部的图（但不知道为啥林晖的那部分代码在我电脑上跑不动所以改了一下，感觉林晖那个更好
                    # print(type(img))
                #print(pic_number)
                if type(img) != type(None):
                    contours, hierachy = locate.detect(img)
                    img=locate.find(img, contours, np.squeeze(hierachy))
                    if type(img) == type(None):
                        print("未检测到定位点")
                    county = lpsize
                    countx = 0

                else:
                    countx = 1020
                    colorstate=3

    #print(bin1)
    print(bintostr(bin1))



def bintostr(s):
    count = 0
    sum = 0
    odd = 0
    outStr = ''
    for i in s:
        if count < 7:
            temp = (ord(i)-ord("0")) * pow(2, 6 - count)
            sum += temp
        if i=='0': odd+=1

        count += 1
        if (count == 8):
            count = 0
            if odd%2==1:
                odd=0
                sum=0
                print("Skip")
                continue

            if(sum==255):
                return outStr
            outStr = outStr + (chr(sum))
            sum = 0
    #print(outStr)
    return outStr



#
if __name__ == "__main__":
    #encode()
    #ffin = FFmpeg(inputs={'': '-f image2 -r 5 -i G:/project1pic/%d.png -y'}, outputs={'test.mp4': None})
    #ffin.run()
    #ffout = FFmpeg(inputs={'': '-i test7.mp4 -r 5 -f image2 -y'}, outputs={'G:/project1outpic/%d.png': None})
    #ffout.run()
    decode()
