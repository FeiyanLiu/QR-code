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
    size = 512  # 图片尺寸
    cube = 16  # 每个单元的大小
    lpsize = cube * 8  # 定位点尺寸 8的倍数
    img = np.ones((size, size), dtype=np.uint8)
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

    img[0:int(lpsize), size - int(lpsize):size] = 255
    img[0:int(lpsize * 7 / 8), size - int(lpsize * 7 / 8):size] = 0
    img[int(lpsize / 8):int(lpsize * 6 / 8), size - int(lpsize * 6 / 8):size - int(lpsize / 8)] = 255
    img[int(lpsize * 2 / 8):int(lpsize * 5 / 8), size - int(lpsize * 5 / 8):size - int(lpsize * 2 / 8)] = 0
    # 右上角
    return img


def encode():
    file = open(r'G:/project1txt/test1.txt', 'rb')
    str1 = file.read()
    print(str1)
    str2 = str2bin(str1)
    size = 512  # 图片尺寸
    cube = 16  # 每个单元的大小
    lpsize = cube * 8  # 定位点尺寸 8的倍数
    countx = 0
    county = lpsize
    QR_number = 1
    QR_print_number = 0
    img = newQrcode(size, lpsize)
    for c in str1:
        b = bin(c).replace('0b', '')
        b = b.rjust(8, '0')
        for b1 in b:
            if countx == size:
                QR_number += 1
                county = lpsize
                countx = 0
            if b1 == '0':
                img[countx:countx + cube, county:county + cube] = 255  # 16*16的小方格视为为一个单位
            else:
                img[countx:countx + cube, county:county + cube] = 0  # 0白1黑
            county += cube
            # 按照区域对于county如何变化分类讨论
            if county == size - lpsize and countx < lpsize - cube:
                county = lpsize
                countx += cube  # 到达下一行
            elif county == size - lpsize and countx == lpsize - cube:
                county = 0
                countx += cube
            elif county == size and countx < size - lpsize - cube:
                county = 0
                countx += cube
            elif county == size and countx == size - lpsize - cube:
                county = lpsize
                countx += cube
            elif county == size and countx >= size - lpsize:
                county = lpsize
                countx += cube
            if countx == size and county == lpsize:
                img=combine_QR_code(img)
                cv2.imwrite(r'G:/project1pic/' + str(QR_number) + '.png', img)
                QR_print_number += 1
                img = newQrcode(512, 128)
    if QR_print_number < QR_number:  # 判断此时是否需要再将图片打印出来
        img = combine_QR_code(img)
        cv2.imwrite(r'G:/project1pic/' + str(QR_number) + '.png', img)


def combine_QR_code(img):
    size = 512  # 图片尺寸
    cube = 16  # 每个单元的大小
    lpsize =128  # 定位点尺寸 8的倍数
    #img=cv2.imread(img_path)
    background=np.ones((size+32,size+32),dtype=np.uint8)*255
    background=cv2.cvtColor(background,cv2.COLOR_GRAY2BGR)
    img=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    for i in range(16, 528):
        for j in range(16, 528):
            background[i, j, 0] = img[i - 16, j - 16, 0]
            background[i, j, 1] = img[i - 16, j - 16, 1]
            background[i, j, 2] = img[i - 16, j - 16, 2]
    return background
    #cv2.imshow("last",background)
    #cv2.waitKey()

def decode():
    img = cv2.imread(r'G:/project1outpic/1.png')
    cv2.imshow("img",img)
    contours, hierachy = locate.detect(img)
    locate.find(img, contours, np.squeeze(hierachy))
    pic_number = 1
    size = 512
    lpsize = 128
    cube = 16
    countx = 0
    county = lpsize
    bin1 = ''
    bin_number = 0
    str1 = ""
    while countx < size:
        if np.sum(img[countx:countx + cube, county:county + cube]) < 32640:  # 这里相当于是取小像素块的平均值，考虑到后面手机拍摄可能会产生色差
            bin1 = bin1 + '1'
        else:
            bin1 = bin1 + '0'
        bin_number += 1
        # print(bin1)
        if bin_number == 8:
            # bin1 = bin1 + " "
            bin_number = 0
        county += cube
        # 这一块的分类讨论和encode是一样的
        if county == size - lpsize and countx < lpsize - cube:
            county = lpsize
            countx += cube  # 到达下一行
        elif county == size - lpsize and countx == lpsize - cube:
            county = 0
            countx += cube
        elif county == size and countx < size - lpsize - cube:
            county = 0
            countx += cube
        elif county == size and countx == size - lpsize - cube:
            county = lpsize
            countx += cube
        elif county == size and countx >= size - lpsize:
            county = lpsize
            countx += cube

        if countx == size and county == lpsize:

            pic_number += 1
            img = cv2.imread(r'G:/project1outpic/' + str(
                pic_number) + '.png')  # 这一段可读性太差，意思是取完全部的图（但不知道为啥林晖的那部分代码在我电脑上跑不动所以改了一下，感觉林晖那个更好
            # print(type(img))

            # print(pic_number)
            if type(img) != type(None):
                contours, hierachy = locate.detect(img)
                locate.find(img, contours, np.squeeze(hierachy))
                county = lpsize
                countx=0
            else:
                countx = 520
    print(pic_number)
    print(bintostr(bin1))

#第一版
# def encode():
#     file=open(r'G:/project1txt/test.txt','rb')
#     str1=file.read()
#     print(str1)
#     str2 = str2bin(str1)
#     countx=128
#     county=128
#     QR_number=1
#     QR_print_number=0
#     img = newQrcode(400,128)
#     for c in str1:
#         b=bin(c).replace('0b','')
#         b=b.rjust(8,'0')
#         for b1 in b:
#             if county == 400:
#                 QR_number+=1
#                 county =128
#             if b1 =='0':img[countx:countx+16,county:county+16]=255     #16*16的小方格视为为一个单位
#             else : img[countx:countx+16,county:county+16]=0            #0白1黑
#             countx+=16
#             if countx == 400:#限制了范围
#                 county+=16
#                 countx=128
#             if county == 400:
#                 cv2.imwrite(r'G:/project1pic/' + str(QR_number) + '.png', img)
#                 QR_print_number+=1
#                 img = newQrcode(400,128);
#     if QR_print_number<QR_number:#判断此时是否需要再将图片打印出来
#         cv2.imwrite(r'G:/project1pic/' + str(QR_number) + '.png', img)

# def decode():
#     img = cv2.imread(r'G:/project1outpic/1.png')
#     pic_number = 1
#     countx = 128
#     county = 128
#     bin1 = ''
#     bin_number = 0
#     str1 = ""
#     while county < 400:
#         if np.sum(img[countx:countx + 16, county:county + 16]) < 32640:  # 这里相当于是取小像素块的平均值，考虑到后面手机拍摄可能会产生色差
#             bin1 = bin1 + '1'
#         else:
#             bin1 = bin1 + '0'
#         bin_number += 1
#         # print(bin1)
#         if bin_number == 8:
#             #bin1 = bin1 + " "
#             bin_number = 0
#         countx += 16
#         if countx == 400:
#             countx = 128
#             county += 16
#         if county == 400:
#             pic_number += 1
#             img = cv2.imread(r'G:/project1outpic/' + str(
#                     pic_number) + '.png')  # 这一段可读性太差，意思是取完全部的图（但不知道为啥林晖的那部分代码在我电脑上跑不动所以改了一下，感觉林晖那个更好
#             # print(type(img))
#             # print(pic_number)
#             if type(img) != type(None):
#                 county = 128
#             else:
#                 county = 500
#     print(bintostr(bin1))

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

    print(outStr)
    return outStr



#
if __name__ == "__main__":
    encode()
    #combine_QR_code(r'G:/project1pic/1.png')
    # ffin = FFmpeg(inputs={'': '-f image2 -r 5 -i G:/project1pic/%d.png -y'}, outputs={'test.mp4': None})
    # ffin.run()
    # ffout = FFmpeg(inputs={'': '-i test1.mp4 -r 5 -f image2 -y'}, outputs={'G:/project1outpic/%d.png': None})
    # ffout.run()
    # decode()
