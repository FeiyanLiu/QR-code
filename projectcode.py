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
        a=bin(c).replace('0b', '')
        a=a.rjust(7,'0')
        #print(a)
        temp.append(a)

    #print (temp)
    str_bin=' '.join(temp)
    return str_bin

def encode():
    file=open(r'G:\project1txt\test.txt','rb')
    str1=file.read()
    str1=str2bin(str1)
    count=0
    print(str1)

    save_file_dir = r'G:\project1pic'
    s = str(count)
    save_dir = save_file_dir + "\\" + s + '.png'
    img = np.zeros((500, 500, 3), np.uint8)
    img.fill(128)
    cv2.imwrite(save_dir, img)
    img = np.zeros((500, 500, 3), np.uint8)
    img.fill(128)
    count+=1
    s = str(count)
    save_dir = save_file_dir + "\\" + s + '.png'
    cv2.imwrite(save_dir, img)

    for i in str1:
        if i=='1':
            img=np.zeros((500,500,3),np.uint8)
            img.fill(255)
            count+=1
            s = str(count)
            save_dir = save_file_dir + "\\" + s + '.png'
            cv2.imwrite(save_dir,img)

        elif i=='0':
            img = np.zeros((500, 500, 3), np.uint8)
            img.fill(0)
            count+=1
            s = str(count)
            save_dir = save_file_dir + "\\" + s + '.png'
            cv2.imwrite(save_dir, img)
        else:continue

    count+=1
    s = str(count)
    save_dir = save_file_dir + "\\" + s + '.png'
    img = np.zeros((500, 500, 3), np.uint8)
    img.fill(128)
    cv2.imwrite(save_dir, img)
    img = np.zeros((500, 500, 3), np.uint8)
    img.fill(128)
    count+=1
    s = str(count)
    save_dir = save_file_dir + "\\" + s + '.png'
    cv2.imwrite(save_dir, img)

def decodebin(decode_img_path):
    image=cv2.imread(decode_img_path)
    (b,g,r)=image[250,250]

    if b==g==r==255:
        return '1'
    elif b==g==r==0:
        return '0'

def bintostr(s):
    count=0
    sum=0
    outStr=''
    for i in s:
        temp=i*pow(2,6-count)
        sum+=temp
        count+=1
        if (count == 7):
           count = 0
           #print(chr(sum))
           outStr = outStr+(chr(sum))
           sum = 0

    #print(outStr)
    return outStr
    #bin_str=''.join([chr(i) for i in [int(b,2) for b in s]])
    #return bin_str

# def encode(code_txt_path,i):
#     qr = qrcode.QRCode(
#         version=5,
#         error_correction=qrcode.constants.ERROR_CORRECT_H,
#         box_size=8,
#         border=4)
#     save_file_dir = r'G:\project1pic'
#     file = open(code_txt_path, "rb")
#     str1 = file.read()
#     img = qrcode.make(str1)
#     s=str(i)
#     save_dir = save_file_dir + "\\" + s + '.png'
#     i += 1
#     #img.save(r'G:\project1pic\1.png')
#     print(save_dir)
#     img.save(save_dir)
#     #img.show()


# def decode_qrcode(code_img_path):
#     if not os.path.exists(code_img_path):
#         raise FileExistsError(code_img_path)
#     # Here, set only recognize QR Code and ignore other type of code
#     imgs = pyzbar.decode(Image.open(code_img_path), symbols=[pyzbar.ZBarSymbol.QRCODE])
#     # print(imgs) #输出详细信息
#     for img in imgs:
#         imgdata = img.data.decode('UTF-8')
#         print(imgdata)


# if __name__ == "__main__":
#     i=1
#     root_dir = r'G:\project1txt'
#     # encode(r'G:\project1txt\1.txt')
#     for file in os.listdir(root_dir):
#         file_name = root_dir + "\\" + file
#         encode(file_name,i)
#         i+=1
#     #out_dir=r'G:\project1txt\test.mp4'
#     ffin=FFmpeg(inputs={'':'-f image2 -r 5 -i G:/project1pic/%d.png -y'},outputs={'test.mp4':None})
#     ffin.run()
#     ffout=FFmpeg(inputs={'':'-i test.mp4 -r 5 -f image2 %d.png -y'},outputs={'G:/project1outpic/%d.png':None})
#     ffout.run()
#     decode_dir=r'G:\project1outpic'
#
#     for file in os.listdir(decode_dir):
#         file_name=decode_dir+"\\"+file
#         decode_qrcode(file_name)
#
#     # decode_qrcode(r'G:\project1pic\1.png')
if __name__ == "__main__":
    encode()
    ffin = FFmpeg(inputs={'': '-f image2 -r 7 -i G:/project1pic/%d.png -y'}, outputs={'test.mp4': None})
    ffin.run()
    ffout = FFmpeg(inputs={'': '-i test.mp4 -r 7 -f image2 %d.png -y'}, outputs={'G:/project1outpic/%7d.png': None})
    ffout.run()
    decode_dir=r'G:\project1outpic'
    outstr=[]
    bitcount=0
    for file in os.listdir(decode_dir):
         file_name=decode_dir+"\\"+file
         if bitcount==7 :
             outstr.append(' ')
             bitcount=0
         #print(file_name)
         ch=decodebin(file_name)

         if ch=='1' or ch=='0' :
             outstr.append(ch)
             bitcount+=1
    #print (outstr)
    strout=''.join(str(outstr))
    newstrout=[]
    for i in strout:
        if i>='0' and i<='9':newstrout.append(int(i))
    #strout=bintostr(strout)
    #newstrout =
    newstrout=bintostr(newstrout)
    #print(strout)
    print(newstrout)

