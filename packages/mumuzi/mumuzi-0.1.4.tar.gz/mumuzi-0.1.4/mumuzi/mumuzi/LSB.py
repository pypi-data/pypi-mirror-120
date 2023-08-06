#author 8神 Cheyenne
from PIL import Image
import math

# 把字节对应转换成二进制字符串
def Byte2Bin(byte, order):
    s = ''
    for i in range(len(byte)):
        if order == 'lsb':
            tmp = str(bin(byte[i]))[2:].zfill(8)
        elif order == 'msb':
            tmp = str(bin(byte[i]))[2:].zfill(8)[::-1]
        else:
            raise(NameError)
        s += tmp
    return(s)

# 把8位二进制数的第n位（从低往高数）替换成0或1
def NumReplace(number, n, x01):
    if number > 255 or number < 0 or n > 7 or n < 0 or x01 not in [0, 1]:
        raise(NameError)
    tmp = str(bin(number))[2:].zfill(8)
    n = 7 - n
    s = tmp[:n] + str(x01) + tmp[n+1:]
    return(int(s, 2))

# 路径-path：源图片和输出图片所在的目录路径
# 源图片-ori，输出图片-out：均为文件名
# 隐写信息载荷-payload：必须为字节类型
# 写入字节位-bit：字符串类型，默认仅写入最低位-'0'，有多位时按排列顺序决定写入顺序
    # 例如'7532'相当于Stegsolve中选择7 5 3 2位和MSBFirst，也相当于zsteg的 -b 10101100
    # 例如'0124'相当于Stegsolve中选择4 2 1 0位和LSBFirst（zsteg不支持LSBFirst）
    # 支持‘1024’这种字节位乱序写入的方式，但Stegsolve和zsteg里没有对应选项或参数
# 写入通道-plane：字符串类型，大写，默认写入RGB通道，按排列顺序决定写入顺序
    # 写入时的顺序是先通道，再字节，即一个通道的所有字节位写完再写下一个通道，所有通道写完再写下一个像素
    # 不支持每个通道写入字节位不同的情况（Stegsolve是支持的，但不常用）
# 坐标读取顺序-axis：默认行优先-x，列优先-y，其他包含倒序的请通过提前翻转源图片实现
# 隐写信息载荷读取顺序-order：按zsteg，默认每8bit从前往后读取-lsb，从后往前读-msb，Stegsolve仅支持lsb
def LSB(path, ori, out, payload, bit = '0', plane = 'RGB', axis = 'x', order = 'lsb'):
    img = Image.open(path + ori)
    w, h, m = img.size[0], img.size[1], img.mode
    binstr = Byte2Bin(payload, order)

    # 把plane参数转换成对应通道的顺序的列表
    plist = []
    for i in plane:
        if m.find(i) == -1:
            raise(IndexError)
        else:
            plist += [m.find(i)]

    # 把bit参数转换成对应字节位的列表
    blist = []
    for i in bit:
        blist += [int(i)]

    # 计算需要的像素数量（不判断图片像素够不够用）
    pixelnum = math.ceil(len(binstr) / (len(plist) * len(bit)))

    # 开始隐写
    for a in range(pixelnum):
        if axis == 'x':
            px, py = a % w, a // w
        elif axis == 'y':
            py, px = a % h, a // h
        else:
            raise(NameError)
        pixel = list(img.getpixel((px, py)))
        for b in range(len(plist)):
            for c in range(len(bit)):
                binstrnum = a * len(plist) * len(bit) + b * len(bit) + c
                if binstrnum < len(binstr):
                    pixel[plist[b]] = NumReplace(pixel[plist[b]], blist[c], int(binstr[binstrnum]))
        img.putpixel((px, py), tuple(pixel))

    img.save(path + out)