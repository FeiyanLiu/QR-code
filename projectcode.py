import os
import time
import sys
from PIL import Image
import qrcode
from pyzbar import pyzbar as pyzbar
from ffmpy3 import FFmpeg
import cv2
import numpy as np
def str2bin(s):
    temp=[]
    for c in s:
        temp.append(bin(c).replace('0b',''))
    str_bin=' '.join(temp)
    return str_bin
def newQrcode():#初始化二维码（一个一个打出来的，三个定位点
    img = np.ones((512, 512), dtype=np.uint8)
    img[0:128, 0:128] = 255
    img[0:112, 0:112] = 0
    img[16:80, 16:80] = 255
    img[32:64, 32:64] = 0

    img[384:512, 0:128] = 255
    img[400:512, 0:112] = 0
    img[432:496, 16:80] = 255
    img[448:480, 32:64] = 0


    img[0:128, 384:512] = 255
    img[0:112, 400:512] = 0
    img[16:80, 432:496] = 255
    img[32:64, 448:480] = 0
    return img
def encode():
    file=open(r'G:/project1txt/test.txt','rb')
    str1=file.read()
    print(str1)
    str2 = str2bin(str1)
    countx=128
    county=128
    QR_number=1
    QR_print_number=0
    img = newQrcode()
    for c in str1:
        b=bin(c).replace('0b','')
        b=b.rjust(8,'0')
        for b1 in b:
            if county == 400:
                QR_number+=1
                county =128
            if b1 =='0':img[countx:countx+16,county:county+16]=255     #16*16的小方格视为为一个单位
            else : img[countx:countx+16,county:county+16]=0            #0白1黑
            countx+=16
            if countx == 400:#限制了范围
                county+=16
                countx=128
            if county == 400:
                cv2.imwrite(r'G:/project1pic/' + str(QR_number) + '.png', img)
                QR_print_number+=1
                img = newQrcode();
    if QR_print_number<QR_number:#判断此时是否需要再将图片打印出来
        cv2.imwrite(r'G:/project1pic/' + str(QR_number) + '.png', img)

def decode():
    img = cv2.imread(r'G:/project1outpic/1.png')
    pic_number = 1
    countx = 128
    county = 128
    bin1 = ''
    bin_number = 0
    str1 = ""
    while county < 400:
        if np.sum(img[countx:countx + 16, county:county + 16]) < 32640:  # 这里相当于是取小像素块的平均值，考虑到后面手机拍摄可能会产生色差
            bin1 = bin1 + '1'
        else:
            bin1 = bin1 + '0'
        bin_number += 1
        # print(bin1)
        if bin_number == 8:
            #bin1 = bin1 + " "
            bin_number = 0
        countx += 16
        if countx == 400:
            countx = 128
            county += 16
        if county == 400:
            pic_number += 1
            img = cv2.imread(r'G:/project1outpic/' + str(
                    pic_number) + '.png')  # 这一段可读性太差，意思是取完全部的图（但不知道为啥林晖的那部分代码在我电脑上跑不动所以改了一下，感觉林晖那个更好
            # print(type(img))
            # print(pic_number)
            if type(img) != type(None):
                county = 128
            else:
                county = 500
    print(bintostr(bin1))

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

    '''
    save_dir = save_file_dir + "/" + s + '.png'
    img.fill(128)
    cv2.imwrite(save_dir, img)
    img = np.zeros((530, 530, 3), np.uint8)
    img.fill(128)
    count+=1
    s = str(count)
    save_dir = save_file_dir + "/" + s + '.png'
    cv2.imwrite(save_dir, img)
    for i in str1:
        if i=='1':
            img=np.zeros((530,530,3),np.uint8)
            img.fill(255)
            count+=1
            s = str(count)
            save_dir = save_file_dir + "/" + s + '.png'
            cv2.imwrite(save_dir,img)
        elif i=='0':
            img = np.zeros((530, 530, 3), np.uint8)
            img.fill(0)
            count+=1
            s = str(count)
            save_dir = save_file_dir + "/" + s + '.png'
            cv2.imwrite(save_dir, img)
        else:continue
    s = str(count)
    save_dir = save_file_dir + "/" + s + '.png'
    img = np.zeros((530, 530, 3), np.uint8)
    img.fill(128)
    cv2.imwrite(save_dir, img)
    img = np.zeros((530, 530, 3), np.uint8)
    img.fill(128)
    count+=1
    s = str(count)
    save_dir = save_file_dir + "/" + s + '.png'
    cv2.imwrite(save_dir, img)
def decodebin(decode_img_path):
    image=cv2.imread(decode_img_path)
    a=(b,g,r)=cv2.split(image)
    if a[0][0][0] ==255:
        return '1'
    elif a[0][0][0]==0:
        return '0'
def bintostr(s):
    bin_str=''.join([chr(i) for i in [int(b,2) for b in s.split(' ')]])
    return bin_str
    '''



if __name__ == "__main__":
    encode()
    ffin = FFmpeg(inputs={'': '-f image2 -r 5 -i G:/project1pic/%d.png -y'}, outputs={'test.mp4': None})
    ffin.run()
    ffout = FFmpeg(inputs={'': '-i test.mp4 -r 5 -f image2 %d.png -y'}, outputs={'G:/project1outpic/%d.png': None})
    ffout.run()
    decode()
    '''
    decode_dir=r'/Users/xianfu/PycharmProjects/project1.1/project1outpic'
    outstr=[]
    bitcount=0
    count = 3
    #print(decodebin(r'/Users/xianfu/PycharmProjects/project1.1/project1outpic/1.png'))
    for file in os.listdir(decode_dir):
         file_name=decode_dir+"/"+str(count)+".png"
         if bitcount==7 :outstr.append(' ')
         ch=decodebin(file_name)
         outstr.append(ch)
         bitcount+=1
         count+=1
    print(outstr)
    strout=''.join(outstr[2:])
    strout=bintostr(strout)
    print(strout)
    '''