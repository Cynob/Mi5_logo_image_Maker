#Downloaded from: https://source.codeaurora.org/quic/la/device/qcom/common/tree/display/logo?h=LA.BR.1.2.7_rb1.1

# Copyright (c) 2013,2015, The Linux Foundation. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#     * Neither the name of The Linux Foundation nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#===========================================================================

#  This script read the logo png and creates the logo.img

# when          who     what, where, why
# --------      ---     -------------------------------------------------------
# 2013-04       QRD     init
# 2015-04       QRD     support the RLE24 compression

# Environment requirement:
#     Python + PIL
#     PIL install:
#         (ubuntu)  sudo apt-get install python-imaging
#         (windows) (http://www.pythonware.com/products/pil/)

# limit:
#    a. This script only support Python 2.7.x, 2.6.x,
#      Can't use in py3x for StringIO module
#    b. This script's input can be a png, jpeg, bmp, gif file.
#    But if it is a gif, only get the first frame by default.
#
# description:
#    struct logo_header {
#       unsigned char[8]; // "SPLASH!!"
#       unsigned width;   // logo's width, little endian
#       unsigned height;  // logo's height, little endian
#       unsigned type;    // 0, Raw Image; 1, RLE24 Compressed Image
#       unsigned blocks;  // block number, real size / 512
#       ......
#    };

#    the logo Image layout:
#       logo_header + Payload data

# ===========================================================================*/
from __future__ import print_function
import sys,os
import struct
import StringIO
from PIL import Image

SUPPORT_RLE24_COMPRESSIONT = 1

## get header
def GetImgHeader(size1, size2, size3, size4, size5, compressed, real_bytes1, real_bytes2, real_bytes3, real_bytes4, real_bytes5):
    SECTOR_SIZE_IN_BYTES = 4096   # Header size
    header = [0 for i in range(SECTOR_SIZE_IN_BYTES)]

    width1, height1 = size1
    width2, height2 = size2
    width3, height3 = size3
    width4, height4 = size4
    width5, height5 = size5
    real_size1 = (real_bytes1  + 4095) / 4096
    real_size2 = (real_bytes1  + real_bytes2  + 4095) / 4096
    real_size3 = (real_bytes1  + real_bytes2  + real_bytes3 + 4095) / 4096
    real_size4 = (real_bytes1  + real_bytes2  + real_bytes3 + real_bytes4 + 4095) / 4096
    real_size5 = (real_bytes1  + real_bytes2  + real_bytes3 + real_bytes4 + real_bytes5 + 4095) / 4096
    
    # magic
    header[:8] = [ord('S'),ord('P'), ord('L'), ord('A'),
                   ord('S'),ord('H'), ord('!'), ord('!')]

    # width1
    header[8] = ( width1        & 0xFF)
    header[9] = ((width1 >> 8 ) & 0xFF)
    header[10]= ((width1 >> 16) & 0xFF)
    header[11]= ((width1 >> 24) & 0xFF)
    # width2
    header[12]= ( width2        & 0xFF)
    header[13]= ((width2 >>  8) & 0xFF)
    header[14]= ((width2 >> 16) & 0xFF)
    header[15]= ((width2 >> 24) & 0xFF)   
    # width3
    header[16]= ( width3        & 0xFF)
    header[17]= ((width3 >> 8 ) & 0xFF)
    header[18]= ((width3 >> 16) & 0xFF)
    header[19]= ((width3 >> 24) & 0xFF)
    # width4
    header[20]= ( width4        & 0xFF)
    header[21]= ((width4 >>  8) & 0xFF)
    header[22]= ((width4 >> 16) & 0xFF)
    header[23]= ((width4 >> 24) & 0xFF)
    # width5
    header[24]= ( width5        & 0xFF)
    header[25]= ((width5 >> 8 ) & 0xFF)
    header[26]= ((width5 >> 16) & 0xFF)
    header[27]= ((width5 >> 24) & 0xFF)

    # height1
    header[28]= ( height1        & 0xFF)
    header[29]= ((height1 >>  8) & 0xFF)
    header[30]= ((height1 >> 16) & 0xFF)
    header[31]= ((height1 >> 24) & 0xFF)
    # height2
    header[32]= ( height2        & 0xFF)
    header[33]= ((height2 >> 8 ) & 0xFF)
    header[34]= ((height2 >> 16) & 0xFF)
    header[35]= ((height2 >> 24) & 0xFF)
    # height3
    header[36]= ( height3        & 0xFF)
    header[37]= ((height3 >>  8) & 0xFF)
    header[38]= ((height3 >> 16) & 0xFF)
    header[39]= ((height3 >> 24) & 0xFF)
    # height4
    header[40]= ( height4        & 0xFF)
    header[41]= ((height4 >> 8 ) & 0xFF)
    header[42]= ((height4 >> 16) & 0xFF)
    header[43]= ((height4 >> 24) & 0xFF)
    # height5
    header[44]= ( height5        & 0xFF)
    header[45]= ((height5 >>  8) & 0xFF)
    header[46]= ((height5 >> 16) & 0xFF)
    header[47]= ((height5 >> 24) & 0xFF)

    #type
    header[48]= ( compressed    & 0xFF)
    #header[49]= 0
    #header[50]= 0
    #header[51]= 0
    header[52]= ( compressed    & 0xFF)
    #header[53]= 0
    #header[54]= 0
    #header[55]= 0
    header[56]= ( compressed    & 0xFF)
    #header[57]= 0
    #header[58]= 0
    #header[59]= 0
    header[60]= ( compressed    & 0xFF)
    #header[61]= 0
    #header[62]= 0
    #header[63]= 0
    header[64]= ( compressed    & 0xFF)
    #header[65]= 0
    #header[66]= 0
    #header[67]= 0

    # block number img 1
    header[68] = ( real_size1        & 0xFF)
    header[69] = ((real_size1 >>  8) & 0xFF)
    header[70] = ((real_size1 >> 16) & 0xFF)
    header[71] = ((real_size1 >> 24) & 0xFF)

    # block number img 2
    header[72] = ( real_size2        & 0xFF)
    header[73] = ((real_size2 >>  8) & 0xFF)
    header[74] = ((real_size2 >> 16) & 0xFF)
    header[75] = ((real_size2 >> 24) & 0xFF)
    
    # block number img 3
    header[76] = ( real_size3        & 0xFF)
    header[77] = ((real_size3 >>  8) & 0xFF)
    header[78] = ((real_size3 >> 16) & 0xFF)
    header[79] = ((real_size3 >> 24) & 0xFF)
    
    # block number img 4
    header[80] = ( real_size4        & 0xFF)
    header[81] = ((real_size4 >>  8) & 0xFF)
    header[82] = ((real_size4 >> 16) & 0xFF)
    header[83] = ((real_size4 >> 24) & 0xFF)
    
    # block number img 5
    header[84] = ( real_size5        & 0xFF)
    header[85] = ((real_size5 >>  8) & 0xFF)
    header[86] = ((real_size5 >> 16) & 0xFF)
    header[87] = ((real_size5 >> 24) & 0xFF)
    output = StringIO.StringIO()
    for i in header:
        output.write(struct.pack("B", i))
    content = output.getvalue()
    output.close()
    return content

def encode(line):
    count = 0
    lst = []
    repeat = -1
    run = []
    total = len(line) - 1
    for index, current in enumerate(line[:-1]):
        if current != line[index + 1]:
            run.append(current)
            count += 1
            if repeat == 1:
                entry = (count+128,run)
                lst.append(entry)
                count = 0
                run = []
                repeat = -1
                if index == total - 1:
                    run = [line[index + 1]]
                    entry = (1,run)
                    lst.append(entry)
            else:
                repeat = 0

                if count == 128:
                    entry = (128,run)
                    lst.append(entry)
                    count = 0
                    run = []
                    repeat = -1
                if index == total - 1:
                    run.append(line[index + 1])
                    entry = (count+1,run)
                    lst.append(entry)
        else:
            if repeat == 0:
                entry = (count,run)
                lst.append(entry)
                count = 0
                run = []
                repeat = -1
                if index == total - 1:
                    run.append( line[index + 1])
                    run.append( line[index + 1])
                    entry = (2+128,run)
                    lst.append(entry)
                    break
            run.append(current)
            repeat = 1
            count += 1
            if count == 128:
                entry = (256,run)
                lst.append(entry)
                count = 0
                run = []
                repeat = -1
            if index == total - 1:
                if count == 0:
                    run = [line[index + 1]]
                    entry = (1,run)
                    lst.append(entry)
                else:
                    run.append(current)
                    entry = (count+1+128,run)
                    lst.append(entry)
    return lst

def encodeRLE24(img):
    width, height = img.size
    output = StringIO.StringIO()

    for h in range(height):
        line = []
        result=[]
        for w in range(width):
            (r, g, b) = img.getpixel((w,h))
            line.append((r << 16)+(g << 8) + b)
        result = encode(line)
        for count, pixel in result:
            output.write(struct.pack("B", count-1))
            if count > 128:
                output.write(struct.pack("B", (pixel[0]) & 0xFF))
                output.write(struct.pack("B", ((pixel[0]) >> 8) & 0xFF))
                output.write(struct.pack("B", ((pixel[0]) >> 16) & 0xFF))
            else:
                for item in pixel:
                    output.write(struct.pack("B", (item) & 0xFF))
                    output.write(struct.pack("B", (item >> 8) & 0xFF))
                    output.write(struct.pack("B", (item >> 16) & 0xFF))
    content = output.getvalue()
    countlenght = len(content)
    while (countlenght % 4096 != 0):
		output.write(struct.pack("B", 0xFF))
		content = output.getvalue()
		countlenght = len(content)
        
    output.close() 
    return content


## get payload data : BGR Interleaved
def GetImageBody(img, compressed=1):
    color = (0, 0, 0)
    if img.mode == "RGB":
        background = img
    elif img.mode == "RGBA":
        background = Image.new("RGB", img.size, color)
        img.load()
        background.paste(img, mask=img.split()[3]) # alpha channel
    elif img.mode == "P" or img.mode == "L":
        background = Image.new("RGB", img.size, color)
        img.load()
        background.paste(img)
        #background.save("splash.png")
    else:
        print ("sorry, can't support this format")
        sys.exit()
    
    background.load()
    
    if compressed == 1:
        return encodeRLE24(background)
    else:
        r, g, b = background.split()
        return Image.merge("RGB",(b,g,r)).tostring()

## make a image

def MakeLogoImage(logo, out):
    img1 = Image.open(logo['infile1'])
    img2 = Image.open(logo['infile2'])
    img3 = Image.open(logo['infile3'])
    img4 = Image.open(logo['infile4'])
    img5 = Image.open(logo['infile5'])
    file = open(out, "wb")
    body1 = GetImageBody(img1, SUPPORT_RLE24_COMPRESSIONT)
    body2 = GetImageBody(img2, SUPPORT_RLE24_COMPRESSIONT)
    body3 = GetImageBody(img3, SUPPORT_RLE24_COMPRESSIONT)
    body4 = GetImageBody(img4, SUPPORT_RLE24_COMPRESSIONT)
    body5 = GetImageBody(img5, SUPPORT_RLE24_COMPRESSIONT)
    file.write(GetImgHeader(img1.size, img2.size, img3.size, img4.size, img5.size, SUPPORT_RLE24_COMPRESSIONT, len(body1), len(body2), len(body3), len(body4), len(body5)))
    file.write(body1)
    file.write(body2)
    file.write(body3)
    file.write(body4)
    file.write(body5)
    file.close()


## mian

def ShowUsage():
    print(" usage: python logo_gen.py [logo1.png] [logo2.png] [logo3.png] [logo4.png] [logo5.png]")

def GetPNGFile():
    infile1 = "logo1.png" #default file name
    infile2 = "logo2.png"
    infile3 = "logo3.png"
    infile4 = "logo4.png"
    infile5 = "logo5.png"
    num = len(sys.argv)
    if num > 7:
        ShowUsage()
        sys.exit(); # error arg

    if num == 6:
        infile1 = sys.argv[1]
        infile2 = sys.argv[2]
        infile3 = sys.argv[3]
        infile4 = sys.argv[4]
        infile5 = sys.argv[5]

    if os.access(infile1, os.R_OK) != True:
        ShowUsage()
        sys.exit(); # error file
    return {'infile1':infile1, 'infile2':infile2, 'infile3':infile3, 'infile4':infile4, 'infile5':infile5 }

if __name__ == "__main__":
    MakeLogoImage(GetPNGFile(), "output/logo.img")
