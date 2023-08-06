# coding: utf-8

from PIL import Image, ImageDraw, ImageFont

CHARS = list("@%#*+=-:. ")


def makeImage(
    imgPath: str,
    savePath: str,
    scale: float = 1,
    fontPath: str = "",
    fontSize: int = 20,
    horzSep=2,
    vertSep=2,
    keepRatio=True,
    keepSize=False,
):
    if not (isinstance(horzSep, int) and isinstance(vertSep, int)):
        raise TypeError("字符的横向间隔及纵向间隔参数数据类型应为整数。")
    if not (0 <= horzSep <= 10 and 0 <= vertSep <= 10):
        raise ValueError("字符横向及纵向间隔参数值大小应在 0 与 10 之间。")
    if not isinstance(scale, (int, float)) or (not 0 < scale <= 1):
        raise ValueError("缩放比例参数的值大小应大于 0 且小于等于 1 。")
    if fontPath:
        imgFont = ImageFont.truetype(fontPath, fontSize)
    else:
        imgFont = ImageFont.load_default()
    ftWidth, ftHeight = imgFont.getsize(CHARS[0])
    # 往图片写入字符时横坐标的移动增量
    hIncrement = ftWidth + horzSep
    # 往图片写入字符时纵坐标的移动增量
    vIncrement = ftHeight + vertSep
    image = Image.open(imgPath).convert("L")
    oldImgWidth, oldImgHeight = image.size
    if keepRatio:
        # 按字符的宽高(加分隔距离)比例来计算原图需要缩放的比例
        imageHeight = round(hIncrement / vIncrement * oldImgHeight)
    imageWidth = round(oldImgWidth * scale)
    imageHeight = round(oldImgHeight * scale)
    if keepRatio or scale != 1:
        image = image.resize((imageWidth, imageHeight), Image.NEAREST)
    lenChars, charList = len(CHARS), list()
    for y in range(imageHeight):
        for x in range(imageWidth):
            grayNum = image.getpixel((x, y))
            charIndex = round((grayNum / 255) * (lenChars - 1))
            charList.append(CHARS[charIndex])
    newWidth = (ftWidth + horzSep) * imageWidth + horzSep
    newHeight = (ftHeight + vertSep) * imageHeight + vertSep
    newImage = Image.new("L", (newWidth, newHeight), 255)
    drawPanel = ImageDraw.Draw(newImage)
    x, y = horzSep, vertSep
    for index, char in enumerate(charList):
        if index != 0 and not (index % imageWidth):
            x = horzSep
            y += vIncrement
        drawPanel.text((x, y), char, 0, imgFont)
        x += hIncrement
    if keepSize:
        newImage = newImage.resize((oldImgWidth, oldImgHeight), Image.BICUBIC)
    newImage.save(savePath)
