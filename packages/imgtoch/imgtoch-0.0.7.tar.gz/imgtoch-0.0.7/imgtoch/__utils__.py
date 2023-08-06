# coding: utf-8

from PIL import Image, ImageDraw, ImageFont

CHARS = list("@%#*+=-:. ")


def makeImage(
    imgPath: str,
    savePath: str,
    scale: float = 1,
    quality: int = 80,
    fontPath: str = "",
    fontSize: int = 14,
    horzSep: int = 2,
    vertSep: int = 2,
    keepRatio=True,
    keepSize=False,
):
    """
    ### 将图片转换为字符图片

    参数 imgPath: str, 源图片的完整路径
    参数 savePath: str, 生成的图片的保存路径，包括文件名
    参数 scale: float, 采集率，大于 0 小于等于 1
    参数 quality: int, 图片保存质量，大于 0 小于等于 100
    参数 fontPath: str, 字体文件路径
    参数 fontSize: int, 字号
    参数 horzSep: int, 字符横向间隔
    参数 vertSep： int, 字符纵向间隔
    参数 keepRatio: bool, 生成的图片是否保持宽高比
    参数 keepSize: bool, 生成的图片是否保持原像素大小
    """
    if not (isinstance(horzSep, int) and isinstance(vertSep, int)):
        raise TypeError("字符的横向间隔及纵向间隔参数数据类型应为整数。")
    if not ((0 <= horzSep <= 10) and (0 <= vertSep <= 10)):
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
    imageWidth = round(oldImgWidth * scale)
    imageHeight = round(oldImgHeight * scale)
    if keepRatio:
        # 按字符的宽高(加分隔距离)比例来计算原图需要缩放的比例
        imageHeight = round(hIncrement / vIncrement * imageHeight)
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
    if keepSize and (newWidth, newHeight) != (oldImgWidth, oldImgHeight):
        newImage = newImage.resize((oldImgWidth, oldImgHeight), Image.BICUBIC)
    newImage.save(savePath, quality=quality)
