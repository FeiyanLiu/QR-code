import cv2
import numpy as np
import glob as gb
import locate
from enum import Enum

class Color(Enum):#状态
    red = 1
    green = 2
    blue = 3


def str2bin(s):
    temp=[]
    for c in s:
        temp.append(bin(c).replace('0b',''))
    str_bin=' '.join(temp)
    return str_bin


def newQrcode(size, lpsize):  # 初始化二维码（一个一个打出来的，三个定位点

    # location point size定位点尺寸
    # print((lpsize*6)/7)
    # 用参数表示每个边的坐标
    size = 1024  # 图片尺寸
    cube = 16  # 每个单元的大小
    lpsize = cube * 14 # 定位点尺寸 8的倍数
    img = np.ones((size, size,3), dtype=np.uint8)
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

def newQrcodewhite(size, lpsize):  # 初始化二维码（一个一个打出来的，三个定位点

    # location point size定位点尺寸
    # print((lpsize*6)/7)
    # 用参数表示每个边的坐标
    size = 1024  # 图片尺寸
    cube = 16  # 每个单元的大小
    lpsize = cube * 14  # 定位点尺寸 8的倍数
    img = np.ones((size, size,3), dtype=np.uint8)
    img[0:size,0:size]=255
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
    #img = np.concatenate(([0,1,2],img, img, img), axis=3)
    #print(img.shape)
    return img

def encode_start():
    size = 1024  # 图片尺寸
    cube = 16  # 每个单元的大小
    lpsize = cube * 14  # 定位点尺寸 8的倍数
    countx = 0
    county = lpsize
    QR_number = 2
    QR_print_number = 0
    img = newQrcodewhite(size, lpsize)
    img=combine_QR_code(img)
    cv2.imwrite(r'/Volumes/LaCie/PythonCode/project1.2/project1pic/' + '1.png', img)
    img = newQrcode(size, lpsize)
    img = combine_QR_code(img)
    cv2.imwrite(r'/Volumes/LaCie/PythonCode/project1.2/project1pic/' + '2.png', img)


def encode():
    file = open(r'/Volumes/LaCie/PythonCode/project1.2/project1txt/test1.txt', 'rb')
    str1 = file.read()
    #print(str1)
    str2 = str2bin(str1)
    #rint(str2)
    size = 1024  # 图片尺寸
    cube = 16  # 每个单元的大小
    lpsize = cube * 14  # 定位点尺寸 8的倍数
    countx = 0
    county = lpsize
    QR_number = 3
    QR_print_number = 0
    QR_c_number=0
    encode_start()
    img = newQrcode(size, lpsize)
    #img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    B,G,R = cv2.split(img)
    colorstate = 0


    for c in str1:
        b = bin(c).replace('0b', '')
        b = b.rjust(8, '0')
        for b1 in b:
            if countx == size :
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
                if colorstate==2:
                    img = combine_QR_code(img)
                    cv2.imwrite(r'/Volumes/LaCie/PythonCode/project1.2/project1pic/' + str(QR_number) + '.png', img)
                    QR_print_number += 1
                    img = newQrcode(1024, 128)
                    colorstate=0
                else:
                    #print(colorstate)
                    colorstate += 1
    if QR_print_number < QR_number:  # 判断此时是否需要再将图片打印出来
        img = combine_QR_code(img)
        cv2.imwrite(r'/Volumes/LaCie/PythonCode/project1.2/project1pic/' + str(QR_number) + '.png', img)


def combine_QR_code(img):
    size = 1024  # 图片尺寸
    cube = 16  # 每个单元的大小
    lpsize =192  # 定位点尺寸 8的倍数
    #img=cv2.imread(img_path)
    background=np.ones((size+32,size+32),dtype=np.uint8)*255
    background=cv2.cvtColor(background,cv2.COLOR_GRAY2BGR)
    #img=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    for i in range(16, 1040):
        for j in range(16, 1040):
            background[i, j, 0] = img[i - 16, j - 16, 0]
            background[i, j, 1] = img[i - 16, j - 16, 1]
            background[i, j, 2] = img[i - 16, j - 16, 2]
    return background
    #cv2.imshow("last",background)
    #cv2.waitKey()

def decode_start(img):
    if(type(img)==type(None)):
        return False
    size = 1024
    lpsize = 192
    cube = 16
    countx = 0
    county = lpsize
    while countx < size:
        # print(np.sum(img[countx:countx + cube, county:county + cube]))
        if np.sum(img[countx:countx + cube, county:county + cube,0]) > 32640:  # 这里相当于是取小像素块的平均值，考虑到后面手机拍摄可能会产生色差
            #print(2)
            return False
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
        return True
def decode():
    #cv2.imshow("img",img)
    pic_number = 1
    size = 1024
    lpsize = 224
    cube = 16
    countx = 0
    county = 224
    bin1 = ''
    str1 = ""
    '''
    img = cv2.imread(r'/Volumes/LaCie/PythonCode/project1.2/project1outpic/1.png')
    contours, hierachy = locate.detect(img)
    img=locate.find(img, contours, np.squeeze(hierachy))
    if(type(img)==type(None)):
        print("未检测到定位点")

    while(not decode_start(img)):
        #print(1)
        pic_number+=1
        img = cv2.imread(r'/Volumes/LaCie/PythonCode/project1.2/project1outpic/' + str(pic_number) + '.png')
        if(type(img) == type(None)):return
        contours, hierachy = locate.detect(img)
        img = locate.find(img, contours, np.squeeze(hierachy))
        while (type(img) == type(None)):
            print("未检测到定位点")
            pic_number+=1
            img = img = cv2.imread(r'/Volumes/LaCie/PythonCode/project1.2/project1outpic/' + str(pic_number) + '.png')
            contours, hierachy = locate.detect(img)
            img = locate.find(img, contours, np.squeeze(hierachy))
        decode_start(img)
    pic_number+=1
'''
    pic_number=3
    img  = cv2.imread(r'/Volumes/LaCie/PythonCode/project1.2/project1outpic/' + str(pic_number) + '.png')
    contours, hierachy = locate.detect(img)
    img = locate.find(img, contours, np.squeeze(hierachy))
    if (type(img) == type(None)):
        print("未检测到定位点")
    colorstate = 0
    count = 101
    while colorstate<2:
        count+=1
        while countx < size:
            #print(np.sum(img[countx:countx + cube, county:county + cube,colorstate]))
            #cv2.imwrite(r'/Users/xianfu/Downloads/103.png', img[countx:, county:,colorstate])
            #exit()
            if np.sum(img[countx:countx + cube, county:county + cube,colorstate]) < 32640:  # 这里相当于是取小像素块的平均值，考虑到后面手机拍摄可能会产生色差
                bin1 = bin1 + '1'
            else:
                bin1 = bin1 + '0'
            #print(bin1)
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
                colorstate+=1
                if colorstate==3:
                    colorstate=0
                    pic_number += 1
                    #countx = 520
                    img = cv2.imread(r'/Volumes/LaCie/PythonCode/project1.2/project1outpic/' + str(
                        pic_number) + '.png')  # 这一段可读性太差，意思是取完全部的图（但不知道为啥林晖的那部分代码在我电脑上跑不动所以改了一下，感觉林晖那个更好
                    # print(type(img))

                    # print(pic_number)
                if type(img) != type(None):
                    contours, hierachy = locate.detect(img)
                    img=locate.find(img, contours, np.squeeze(hierachy))
                    county = lpsize
                    countx = 0

                else:
                    countx = 1032
                    colorstate = 3
    print(bin1)
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
    print(outStr)
    return outStr



#
if __name__ == "__main__":
    encode()
    #ffin = FFmpeg(inputs={'': '-f image2 -r 5 -i /Volumes/LaCie/PythonCode/project1.2/project1pic/%d.png -y'}, outputs={'test1.mp4': None})
    #ffin.run()
    #ffout = FFmpeg(inputs={'': '-i test1.mp4 -r 5 -f image2  -y'}, outputs={'/Volumes/LaCie/PythonCode/project1.2/project1outpic/%d.png': None})
    #ffout.run()
    #decode()
