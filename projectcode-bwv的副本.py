import os
import time
import sys
from ffmpy3 import FFmpeg
import cv2
import numpy as np
import struct
import glob as gb
import locate
from tkinter import messagebox
from tkinter.filedialog import *
import crc8

wrong = []
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
    size = 1000  # 图片尺寸
    cube = 20  # 每个单元的大小
    lpsize = 200  # 定位点尺寸 8的倍数
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
    size = 1000  # 图片尺寸
    cube = 20 # 每个单元的大小
    lpsize = 200 # 定位点尺寸 8的倍数
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
    return img

def encode_start(video_path):
    size = 1000  # 图片尺寸
    cube = 20  # 每个单元的大小
    lpsize = 200  # 定位点尺寸 8的倍数
    countx = 0
    county = lpsize
    QR_number = 2
    QR_print_number = 0
    img = newQrcodewhite(size, lpsize)
    img=combine_QR_code(img)
    cv2.imwrite(video_path+'/'+ '1.png', img)
    img = newQrcode(size, lpsize)
    img = combine_QR_code(img)
    cv2.imwrite(video_path+'/'+ '2.png', img)


def encode(text_path,video_path,max_second):
    file = open(text_path, 'rb')
    str1 = file.read()
    lens=len(str1)
    str2 = []
    #for i in range(0,lens,5):
     #   a=str1[i]-
    #print(str1)
    #str2 = str2bin(str1)
    size = 1000  # 图片尺寸
    cube = 20  # 每个单元的大小
    lpsize = 200  # 定位点尺寸 8的倍数
    countx = 0
    county = lpsize
    QR_number = 3
    QR_print_number = 0
    encode_start(video_path)
    img = newQrcode(size, lpsize)
    #B, G, R = cv2.split(img)
    colorstate = 0
    crc_count = 0
    crc_data=""
    max_Frame=max_second*5+2
    print(str1)
    for c in str1:
        crc_count += 1
        print(c)
        if (crc_count % 10 != 0):
            b = bin(c).replace('0b', '')
            b = b.rjust(8, '0')
            crc_data+=b
        if (crc_count % 10 == 0) or crc_count == len(str1):
            #print(crc_data)
            b = bin(c).replace('0b', '')
            b = b.rjust(8, '0')
            crc_data += b
            crc = crc8.en_crc8(crc_data)
            b = b + crc
            crc_data = ""
        print(b)
        for b1 in b:
            if countx == size:
                if colorstate==0:
                    QR_number += 1
                    if (QR_number > max_Frame): break
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
                    img=combine_QR_code(img)
                    cv2.imwrite(video_path +'/'+ str(QR_number) + '.png', img)
                    QR_print_number += 1
                    img = newQrcode(1000, 200)
                    colorstate=0
                else: colorstate+=1
    if QR_print_number < QR_number:  # 判断此时是否需要再将图片打印出来
        img = combine_QR_code(img)
        cv2.imwrite(video_path+'/' + str(QR_number) + '.png', img)
    video_path+='/'
    ffin = FFmpeg(inputs={'': '-f image2 -r 5 -i '+video_path+'/%d.png -y'}, outputs={video_path+'test.mp4': None})
    ffin.run()


def combine_QR_code(img):
    size = 1000  # 图片尺寸
    cube = 20  # 每个单元的大小
    lpsize =200  # 定位点尺寸 8的倍数
    #img=cv2.imread(img_path)
    background=np.ones((size+40,size+40,3),dtype=np.uint8)*255
    #background=cv2.cvtColor(background,cv2.COLOR_GRAY2BGR)
    #img=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    for i in range(20, 1020):
        for j in range(20, 1020):
            background[i, j] = img[i - 20, j - 20]
            background[i, j] = img[i - 20, j - 20]
            background[i, j] = img[i - 20, j - 20]
    return background
    #cv2.imshow("last",background)
    #cv2.waitKey()



def decode_start(img):
    if(type(img)==type(None)):
        return False
    size = 1000

    lpsize = 200
    cube = 20
    countx = 0
    county = lpsize
    while countx < size:
        #print(np.sum(img[countx:countx + cube, county:county + cube]))
        if np.sum(img[countx:countx + cube, county:county + cube]) > 180000:  # 这里相当于是取小像素块的平均值，考虑到后面手机拍摄可能会产生色差
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

def decode(video_path,pic_path,txt_path,check_path):
    #cv2.imshow("img",img)

    ffout = FFmpeg(inputs={'': '-i '+video_path+' -r 5 -f image2 -y'}, outputs={pic_path+'/%d.png': None})
    ffout.run()

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


    img = cv2.imread(pic_path+'/1.png')
    if(type(img)==type(None)):
        print("end1")
        print(bintostr(bin1))
        with open(txt_path + '/out.bin', 'wb')as f:
            f.write(bytes(bintostr(bin1), encoding='utf-8'))
        comparison()
        return
    contours, hierachy = locate.detect(img)
    img=locate.find(img, contours, np.squeeze(hierachy))
    #cv2.imshow("2",img)
    while (type(img) == type(None)):
        print('未检测到定位点1'+ '/' + str(pic_number))
        pic_number += 1
        print(pic_number)
        img = cv2.imread(pic_path + '/' + str(pic_number) + '.png')
        if (type(img) == type(None)):
            print("end2")
            print(bintostr(bin1))
            with open(txt_path + '/out.bin', 'wb')as f:
                f.write(bytes(bintostr(bin1), encoding='utf-8'))
            comparison()
            return
        contours, hierachy = locate.detect(img)
        img = locate.find(img, contours, np.squeeze(hierachy))

    while(not decode_start(img)):
        pic_number+=1
        print(pic_number)
        img = cv2.imread(pic_path+'/' + str(pic_number) + '.png')
        if(type(img) == type(None)):
            print("end3")
            with open(txt_path + '/out.bin', 'wb')as f:
                f.write(bytes(bintostr(bin1), encoding='latin1'))
            return
        contours, hierachy = locate.detect(img)
        img = locate.find(img, contours, np.squeeze(hierachy))
        while (type(img) == type(None)):
            print('未检测到定位点2'+ '/' + str(pic_number))
            pic_number+=1
            print(pic_number)
            img = cv2.imread(pic_path+'/' + str(pic_number) + '.png')
            if (type(img) == type(None)):
                print('end4')
                with open(txt_path + '/out.bin', 'wb')as f:
                    f.write(bytes(bintostr(bin1), encoding='latin1'))
                return
            contours, hierachy = locate.detect(img)
            img = locate.find(img, contours, np.squeeze(hierachy))
        decode_start(img)
    pic_number+=1
    #print(pic_number)

    #pic_number=7
    img  = cv2.imread(pic_path+'/' + str(pic_number) + '.png')
    if (type(img) == type(None)):
        print('end5')
        #print(bintostr(bin1))
        with open(txt_path + '/out.bin', 'wb')as f:
            f.write(bytes(bintostr(bin1), encoding='latin1'))
        comparison()
        return
    #cv2.imshow("img",img)
    contours, hierachy = locate.detect(img)
    img = locate.find(img, contours, np.squeeze(hierachy))
    if (type(img) == type(None)):
        print('未检测到定位点3' + '/' + str(pic_number))

    #print(pic_number)

    count+=1
    colorstate=0
    while colorstate < 3:
        count += 1
        while countx < size:
            # print(type(img))
            # print(colorstate)
            # print(np.sum(img[countx:countx + cube, county:county + cube,colorstate]))
            if np.sum(img[countx:countx + cube, county:county + cube,
                      colorstate]) < 56000:  # 这里相当于是取小像素块的平均值，考虑到后面手机拍摄可能会产生色差
                bin1 = bin1 + '1'
            else:
                bin1 = bin1 + '0'
            # print(bin1)
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
                colorstate += 1
                # print(colorstate)
                if colorstate == 3:
                    colorstate = 0
                    pic_number += 1
                    # countx = 520
                    print(pic_number)
                    img = cv2.imread(pic_path + '/' + str(
                        pic_number) + '.png')  # 这一段可读性太差，意思是取完全部的图（但不知道为啥林晖的那部分代码在我电脑上跑不动所以改了一下，感觉林晖那个更好
                    # print(type(img))
                # print(pic_number)
                if type(img) != type(None):
                    contours, hierachy = locate.detect(img)
                    img = locate.find(img, contours, np.squeeze(hierachy))
                    while type(img) == type(None):
                        print('未检测到定位点4' + '/' + str(pic_number))
                        pic_number += 1
                        img = cv2.imread(pic_path + '/' + str(
                            pic_number) + '.png')
                        if (type(img) == type(None)):
                            print("end6")
                            countx = 1150
                            colorstate = 3
                            print(bintostr(bin1))
                            with open(txt_path + '/out.bin', 'wb')as f:
                                f.write(bytes(bintostr(bin1), encoding='latin1'))
                            comparison()
                            return
                        else:
                            contours, hierachy = locate.detect(img)
                            img = locate.find(img, contours, np.squeeze(hierachy))
                    county = lpsize
                    countx = 0

                else:
                    print("end7")
                    countx = 1150
                    colorstate = 3

    #print(bin1)
    output = ""
    for i in range(0,len(bin1)-1,88):
        #print(len(bin1),i,i+87)
        flag = 0
        if i+87>len(bin1):
            #output += bin1[i:-8]
            output+=crc8.de_crc8(bin1[i:])
            flag = crc8.de_crc8(bin1[i])
        else:
             #print(bin1[i:i+63])
             #output += bin1[i:i+80]
             #flag = crc8.de_crc8(bin1[i:i+88])
             output += crc8.de_crc8(bin1[i:i+88])
        #if flag == 1: wrong.append(i)
        #print(output)
    print(bintostr(output))
    with open(txt_path + '/out.bin', 'wb')as f:
        f.write(bintostr(output))
    comparison()


def comparison():
    with open(outPath1.get() + '/out.bin', 'rb') as file1:
        contents1 = file1.readlines()  # 读取每一行 存为一个列表

    with open(textPath.get(), 'rb') as file2:
        contents2 = file2.readlines()
    print(contents1)
    print(contents2)
    # 打开编码前的文件和解码后的文件
    with open(outPath2.get() + '/vout.bin', 'wb') as fileOut:  # 创建文件并输出结果
        j = 0
        i = 0
        for line in contents1:  # 解码文件中的每一行
            right = '1'
            error = '0'
            line = line.decode("latin1")
            for c in line:  # 每一行中的每一个字符
                # if (len(contents2[i]) >= j + 1):
                print(ord(c),contents2[i][j])
                judge = ''
                if (c == ' ' and contents2[i][j] != 32):
                    judge = '00000000'
                    print("find!")
                elif (ord(c) == contents2[i][j]):
                    judge = '11111111'
                    print("correct!")
                else:
                    s1 = bin(ord(c)).replace('0b', '').rjust(8, '0')  # 把c转为8位二进制
                    # print(s1)
                    s2 = bin(contents2[i][j]).replace('0b', '').rjust(8, '0')
                    # print(s2)
                    for k in range(0, 8):
                        if (s1[k] == s2[k]):
                            # print(s1[k],s2[k])
                            judge += right
                        else:
                            judge += error
                    print("wrong!")
                fileOut.write(struct.pack('B', int(judge, 2)))
                j = j + 1
                #print(ord(c), contents2[i][j],"333")
                if (len(contents2[i]) == j):  # 为防止越界 有可能原本的文件比较短
                    i = i + 1
                    j = 0
                    print(ord(c), contents2[i][j], "*****")
'''
def comparison():

    with open(outPath1.get()+'/out.bin', 'rb') as file1:
        contents1 = file1.readlines()#读取每一行 存为一个列表

    with open(textPath.get(),'rb') as file2:
        contents2= file2.readlines()
    print(contents1)
    print(contents2)
    #打开编码前的文件和解码后的文件
    with open (outPath2.get()+'/vout.bin','wb') as fileOut :#创建文件并输出结果
        i = 0
        for line in contents1:  # 解码文件中的每一行
            if (len(contents2) > i):  # 如果原本的文件有第i行
                j = 0
                right = '1'
                error = '0'
                line=line.decode("latin1")
                for c in line:  # 每一行中的每一个字符
                    if (len(contents2[i]) >= j + 1):
                        print(c,contents2[i][j])
                    judge = ''
                    if (len(contents2[i]) < j + 1):  # 为防止越界 有可能原本的文件比较短
                        judge = '00000000'
                        print(1,j,len(contents2[i]))
                    elif (c==' ' and contents2[i][j]!=32):
                        judge = '00000000'
                        print("find!")
                    elif (c == chr(contents2[i][j])):
                        judge = '11111111'
                        print("correct!")
                    else:
                        s1 = bin(ord(c)).replace('0b', '').rjust(8, '0')  # 把c转为8位二进制
                        #print(s1)
                        s2 = bin(contents2[i][j]).replace('0b', '').rjust(8, '0')
                        #print(s2)
                        for k in range(0, 8):
                            if (s1[k] == s2[k]):
                                # print(s1[k],s2[k])
                                judge += right
                            else:
                                judge += error
                        print("wrong!")

                    #print("is "+judge)
                    fileOut.write(struct.pack('B', int(judge, 2)))
                    j += 1
                if (len(contents2[i]) > len(contents1[i])):
                    for c in range(0, len(contents2[i]) - len(contents1[i])):
                        judge = '00000000'  # 这里处理解码文本比原文本更短的情况 短a个比特就输出a个0
                        fileOut.write(struct.pack('B', int(judge, 2)))
            i += 1
        if (len(contents2) > len(contents1)):
            for c in range(0, len(contents2) - len(contents1)):
                for d in range(0, len(contents2[len(contents1) + c])):
                    judge = '00000000'
                    fileOut.write(struct.pack('B', int(judge, 2)))
        elif (len(contents2) < len(contents1)):
            for c in range(0, len(contents1) - len(contents2)):
                for d in range(0, len(contents1[len(contents2) + c])):
                    judge = '00000000'
                    fileOut.write(struct.pack('B', int(judge, 2)))
'''




def bintostr(s):
    count = 0
    sum = 0
    odd = 0
    outStr = b''
    #print(s)
    for i in s:
        #print(i)
        if count < 8:
            temp = (ord(i)-ord("0")) * pow(2, 7 - count)
            sum += temp
            count += 1
        if (count == 8):
            #print("H")
            count = 0

            #print(hex(sum))
            print(bytes(chr(sum),encoding='latin1'))
            outStr += bytes(chr(sum),encoding='latin1')
            #print((bin(sum)))
            sum = 0

    return outStr



#
if __name__ == "__main__":
    #encode()
    #ffin = FFmpeg(inputs={'': '-f image2 -r 10 -i G:/project1pic/%d.png -y'}, outputs={'test.mp4': None})
    #ffin.run()
    #ffout = FFmpeg(inputs={'': '-i test10.mp4 -r 10 -f image2 -y'}, outputs={'G:/project1outpic/%d.png': None})
    #ffout.run()
    #decode()

    root = Tk()
    root.title('QR code')
    textPath = StringVar()
    videoPath = StringVar()
    video_IN= StringVar()
    pic_IN=StringVar()
    outPath1 = StringVar()
    outPath2 = StringVar()
    video_second = StringVar()

    # 选取文件路径
    def selectFilePath():
        path_ = askopenfilename()
        textPath.set(path_)


    # 选取文件夹路径
    def selectDirectoryPath():
        path_ = askdirectory()
        videoPath.set(path_)


    def decode_button():
        print("decode")
        video_path=video_IN.get()
        pic_path=pic_IN.get()
        txt_path=outPath1.get()
        check_path=outPath2.get()
        decode(video_path,pic_path,txt_path,check_path)
        i = messagebox.showinfo('消息框', '解码完成！请到相关路径下查看文件！')
        print(i)  # 解码结束设置弹框提醒


    def encode_button():
        print("encode")
        textpath=textPath.get()
        print(textpath)
        videopath=videoPath.get()
        second=video_second.get()
        max_second=int(second)
        encode(textpath,videopath,max_second)

        i = messagebox.showinfo('消息框', '编码完成！请到相关路径下查看文件！')
        print(i)  # 编码结束设置弹框提醒

    def decode_video_path():
        path_ = askopenfilename()
        video_IN.set(path_)


    def decode_pic_path():
        path_ = askdirectory()
        pic_IN.set(path_)

    def decode_text_path1():
        path_ = askdirectory()
        outPath1.set(path_)

    def decode_text_path2():
        path_ = askdirectory()
        outPath2.set(path_)

    Label(root, text="上传二进制文件:").grid(row=1, column=1, padx=20, pady=20, stick=E)
    Entry(root, textvariable=textPath).grid(row=1, column=3, padx=20, pady=20)
    Button(root, text="路径选择", command=selectFilePath).grid(row=1, column=4)
    Label(root, text="保存编码视频:").grid(row=3, column=1, padx=20, pady=20, stick=E)
    Entry(root, textvariable=videoPath).grid(row=3, column=3, padx=20, pady=20)
    Label(root, text="目标视频长度（秒）:").grid(row=4, column=1, padx=20, pady=20, stick=E)
    Entry(root, textvariable=video_second).grid(row=4, column=3, padx=20, pady=20)
    Button(root, text="路径选择", command=selectDirectoryPath).grid(row=3, column=4)
    Button(root, text="   确认   ", command=encode_button).grid(row=5, column=4, padx=20, pady=20, stick=E)  # 点击确认启动编码
    Label(root, text="上传解码视频:").grid(row=7, column=1, padx=20, pady=20, stick=E)
    Entry(root, textvariable=video_IN).grid(row=7, column=3, padx=20, pady=20)
    Button(root, text="路径选择", command=decode_video_path).grid(row=7, column=4)

    Label(root, text="保存视频图片:").grid(row=8, column=1, padx=20, pady=20, stick=E)
    Entry(root, textvariable=pic_IN).grid(row=8, column=3, padx=20, pady=20)
    Button(root, text="路径选择", command=decode_pic_path).grid(row=8, column=4)


    Label(root, text="保存解码文本:").grid(row=9, column=1, padx=20, pady=20, stick=E)
    Entry(root, textvariable=outPath1).grid(row=9, column=3, padx=20, pady=20)
    Button(root, text="路径选择", command=decode_text_path1).grid(row=9, column=4)
    Label(root, text="保存对比文件:").grid(row=11, column=1, padx=20, pady=20, stick=E)
    Entry(root, textvariable=outPath2).grid(row=11, column=3, padx=20, pady=20)
    Button(root, text="路径选择", command=decode_text_path2).grid(row=11, column=4)
    Button(root, text="   确认   ", command=decode_button).grid(row=13, column=4, padx=20, pady=20, stick=E)  # 点击确认启动解码

    root.mainloop()