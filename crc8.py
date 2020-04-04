from binascii import unhexlify


def str2bin(s):
    temp = []
    for c in s:
        # print(bin(ord(c)))
        temp.append(bin(ord(c)).replace('0b', '').rjust(8, '0'))
    str_bin = ''.join(temp)
    return str_bin


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
                crc = (crc << 1) ^ DI
            else:
                crc = (crc << 1) ^ 0
        crc8_table.append(crc & 0xFF)


def crc8(buf, n):
    crc_r = 0
    if not (len(crc8_table)):
        init_crc8()
    for i in range(n):
        crc_r = crc8_table[crc_r ^ buf[i]]
        crc_r &= 0xFF
    crc = bin(~crc_r & 0xFF).replace("0b", "").rjust(8, '0')
    return crc


def en_crc8(data):
    new_data = ""
    l = len(data)
    for i in range(0, l, 8):
        # print(i)
        a = hex(int(data[i:i + 8], 2)).replace("0x", "").rjust(2, '0')
        # print(a)
        new_data += a
    # print(new_data)
    send_data = unhexlify(bytes(new_data, "LATIN1"))
    # print(send_data)
    crc = crc8(send_data, len(send_data)).rjust(8, '0')
    print()
    return crc


def en_s_crc8(y):
    data = str2bin(y)
    new_data = hex(int(data, 2)).replace("0x", "")
    send_data = unhexlify(bytes(new_data, "UTF-8"))
    # print(send_data)
    crc = crc8(send_data, len(send_data)).rjust(8, '0')
    return crc


def de_crc8(data):
    flag = 0
    crc = en_crc8(data[:-8])
    # print(data,crc,data[-8:])
    for i in range(8):
        if crc[i] != data[-8 + i]:
            flag = 1
            break;
    '''
    if flag==1:

         a = ""
         c = int((len(data)-8)/8)
         for i in range(c):
             a+="01000001"
         #print(a)

         return True
    else: 
         return False
         #print(data[:-8])
    '''
    return flag


if __name__ == '__main__':
    print(str2bin('1Our diurn'))
    print(en_crc8("00110001010011110111010101110010001000000110010001101001011101010111001001101110"))
    # print(de_crc8('0011000101001111011101010111001000100000011001000110100101110101011100100110111000001000'),len('1001001110111001000001001010111010111011101100101010000010000101'))
    # 1001001110111001000001001010111010111011101100101010000010000101
    # 100100111011100100000100101011101011101110110010101000001000010
    # 100100111011100100000100101011101011101110110010101000001
    # 1001001110111001000001001010111010111011101100101010000010000101
    # 1001001110111001000001001010111010111011101100101010000
    # 10010101011000000001001000001100101111010011000110101110000101000111011111111111111111111
    # 01000001100101111010011000110101110000101000111011
    # 11010011100111110010111011101100011110010101011000000001001000001100101111010011000110101110000101000111011111111
