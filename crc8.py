'''
def crc_1byte(data):
    crc_1byte = 0

    for i in range(0,8):
        if((crc_1byte^data)&0x01):
            crc_1byte^=0x18
            crc_1byte>>=1
            crc_1byte|=0x80
        else:
            crc_1byte>>=1
        return crc_1byte

def crc_byte(data):
    ret=0
    for byte in data:
        ret = (crc_1byte(ret^byte))
    return ret

if __name__ == '__main__':
    a = [1,5,9,6,4,2,1,3,1,1,2]
    c = crc_byte(a)
    print(bin(c))
'''

__author__ = 'Administrator'

from binascii import unhexlify

DI = 0x07
crc8_table = []

def init_crc8():
    for i in range(256):
        crc = i
        for j in range(8):
            tmp = crc & 0x80
            if tmp:
                crc = (crc << 1)^DI
            else:
                crc = (crc << 1)^0
        crc8_table.append(crc&0xFF)

def crc8(buf,n):
    crc_r=0
    if not(len(crc8_table)):
        init_crc8()
    for i in range (n):
        crc_r = crc8_table[crc_r^buf[i]]
        crc_r &= 0xFF
    crc = bin(~crc_r & 0xFF).replace("0b","").rjust(8,'0')
    return crc

def en_crc8(data):
    new_data = ""
    send = ""
    for c in data:
        #print(c)
        new_data += hex(ord(c)).replace("0x", "").rjust(2,'0')
        send += bin(ord(c)).replace("0b", "").rjust(7, '0')
    #print(new_data)
    send_data = unhexlify(bytes(new_data, "ASCII"))
    #print(send_data)
    crc = crc8(send_data, len(send_data)).rjust(8, '0')
    #print(len(crc))
    #print(send)
    #print(crc)
    send = send+crc
    #print(send)
    #print(len(send))
    return crc

def de_crc8(data):
    count = 0
    sum = 0
    outStr = ''
    flag = 0
    #print(data[:-8])
    for i in data[:-8]:
        # print(i)
        temp = (ord(i) - ord("0")) * pow(2, 6 - count)
        sum += temp
        count += 1
        if (count == 7):
            # print("H")
            count = 0
            if (sum == 127):
                flag+=1
                break;
            else:
                outStr = outStr + (chr(sum))
            #print(outStr)
            sum = 0
    crc = en_crc8(outStr)
    #print("*")
    #print(outStr)
    #print(crc)
    #print(data[-8:])

    if (outStr!=''):
        if flag==0:
            for i in range(8):
                #print(i)
                #print(crc[i],data[-8+i])
                if crc[i]!=data[-8+i]:
                    outStr="*"
                    break;
        if flag > 0:
            print(flag)
            i = (7 - flag)*7 + 8
            new_data = data[:i]
            print(data)
            print(new_data)
    else:
        #print("$$")
        outStr=""
    return outStr

if __name__ == '__main__':
    print(en_crc8("In June "))
    print(de_crc8('1001001110111001000001001010111010111011101100101010000010000101'),len('1001001110111001000001001010111010111011101100101010000010000101'))
                   #1001001110111001000001001010111010111011101100101010000010000101
                   #100100111011100100000100101011101011101110110010101000001000010
                   #100100111011100100000100101011101011101110110010101000001
                   #1001001110111001000001001010111010111011101100101010000010000101
                   #1001001110111001000001001010111010111011101100101010000
                   #10010101011000000001001000001100101111010011000110101110000101000111011111111111111111111
                                        #01000001100101111010011000110101110000101000111011
                                        #11010011100111110010111011101100011110010101011000000001001000001100101111010011000110101110000101000111011111111
                                                                                                                             #0101110000101000111011