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
    file=open(r'/Users/xianfu/PycharmProjects/project1.1/project1txt/test.txt','rb')
    str1=file.read()
    str2 = str2bin(str1)
    countx=128
    county=128
    QR_number=1
    QR_print_number=0
    img = newQrcode()
    for c in str1:
        b=bin(c).replace('0b','')
        if len(b)==6: b = "00"+b
        elif len(b)==7 : b = "0"+b
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
                cv2.imwrite(r'/Users/xianfu/PycharmProjects/project1.1/project1pic/' + str(QR_number) + '.png', img)
                QR_print_number+=1
                img = newQrcode();
    if QR_print_number<QR_number:#判断此时是否需要再将图片打印出来
        cv2.imwrite(r'/Users/xianfu/PycharmProjects/project1.1/project1pic/' + str(QR_number) + '.png', img)

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
    ffin = FFmpeg(inputs={'': '-f image2 -r 5 -i /Users/xianfu/PycharmProjects/project1.1/project1pic/%d.png -y'}, outputs={'/Users/xianfu/PycharmProjects/project1.1/test.mp4': None})
    ffin.run()
    ffout = FFmpeg(inputs={'': '-i test.mp4 -r 5 -f image2 %d.png -y'}, outputs={'/Users/xianfu/PycharmProjects/project1.1/project1outpic/%d.png': None})
    ffout.run()
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