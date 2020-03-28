
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

def de_crc8(data):
    flag = 0
    crc = en_crc8(data[:-8])
    for i in range(8):
        if crc[i]!=data[-8+i]:
            flag=1
            break;
    if flag==1:
        return ""
    else:
        return data[:-8]

if __name__ == '__main__':
    print(en_crc8("In June "))
    print(de_crc8('1001001110111001000001001010111010111011101100101010000010000101'),
    
