# coding: utf-8

from typing import Tuple

from PIL import Image, ImageDraw, ImageFont


def makeImage(
    imgPath: str,
    savePath: str,
    chars: str = None,
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
    参数 chars: str, 用于图像的字符表，字符数应大于 1，无需事先排序
    参数 scale: float, 采集率，大于 0 小于等于 1
    参数 quality: int, 图片保存质量，大于 0 小于等于 100
    参数 fontPath: str, 字体文件路径
    参数 fontSize: int, 字体大小
    参数 horzSep: int, 字符横向间隔
    参数 vertSep： int, 字符纵向间隔
    参数 keepRatio: bool, 生成的图片是否保持宽高比
    参数 keepSize: bool, 生成的图片是否保持原像素大小
    """
    if chars is None:
        chars = "HdRQA#PXCFJIv?!+^-:. "
    if not isinstance(chars, str):
        raise TypeError("用于图像的字符表参数值类型必须是字符串类型。")
    if len(chars) < 2:
        raise ValueError("用于图像的字符表中字符个数不能少于 2 个。")
    if not isinstance(scale, (int, float)) or (not 0 < scale <= 1):
        raise ValueError("缩放比例参数的值大小应大于 0 且小于等于 1 。")
    if not (isinstance(horzSep, int) and isinstance(vertSep, int)):
        raise TypeError("字符的横向间隔及纵向间隔参数数据类型应为整数。")
    if not ((0 <= horzSep <= 10) and (0 <= vertSep <= 10)):
        raise ValueError("字符横向及纵向间隔参数值大小应在 0 与 10 之间。")
    if fontPath:
        imgFont = ImageFont.truetype(fontPath, fontSize)
    else:
        imgFont = ImageFont.load_default()
    chars = sortByGrayscale(chars, fontPath, fontSize)
    fontWidth, fontHeight = imgFont.getsize(chars[0])
    image = Image.open(imgPath).convert("L")
    oldImgWidth, oldImgHeight = image.size
    imageWidth = round(oldImgWidth * scale)
    imageHeight = round(oldImgHeight * scale)
    # 往图片写入字符时横坐标及纵坐标的移动增量
    incrementX, incrementY = fontWidth + horzSep, fontHeight + vertSep
    if keepRatio:
        # 按字符的宽高(加分隔距离)比例来计算原图需要缩放的比例
        imageHeight = round(incrementX / incrementY * imageHeight)
    if keepRatio or scale != 1:
        image = image.resize((imageWidth, imageHeight), Image.NEAREST)
    newWidth = (fontWidth + horzSep) * imageWidth + horzSep
    newHeight = (fontHeight + vertSep) * imageHeight + vertSep
    newImage = Image.new("L", (newWidth, newHeight), 255)
    drawPanel = ImageDraw.Draw(newImage)
    pointX, pointY, lenChars = horzSep, vertSep, len(chars)
    for y in range(imageHeight):
        for x in range(imageWidth):
            grayValue = image.getpixel((x, y))
            charIndex = round(grayValue / 255 * (lenChars - 1))
            drawPanel.text((pointX, pointY), chars[charIndex], 0, imgFont)
            pointX += incrementX
        pointX = horzSep
        pointY += incrementY
    if keepSize and (newWidth, newHeight) != (oldImgWidth, oldImgHeight):
        newImage = newImage.resize((oldImgWidth, oldImgHeight), Image.BICUBIC)
    newImage.save(savePath, quality=quality)


def grayscaleOf(char: str, fontPath: str = "", fontSize: int = 14) -> Tuple[str, int]:
    """
    ### 返回给定单字符在给定字体时的 (字符, 等效灰度值) 元组

    参数 char: str，单字符
    参数 fontPath: str，字体文件路径，可省略
    参数 fontSize: int，字体大小，仅在指定字体文件时生效，可省略

    返回值：tuple，(字符, 灰度值)元组
    """
    if not isinstance(char, str) or len(char) != 1:
        raise ValueError("字符参数'char'值必须为单个字符。")
    if not isinstance(fontPath, str):
        raise TypeError("字体路径必须为字符串。")
    if not fontPath:
        imgFont = ImageFont.load_default()
    else:
        imgFont = ImageFont.truetype(fontPath, fontSize)
    fontWidth, fontHeight = imgFont.getsize(char)
    newImage = Image.new("L", (fontWidth, fontHeight), 255)
    drawPanel = ImageDraw.Draw(newImage)
    drawPanel.text((0, 0), char, 0, imgFont)
    grayscaleValues = (
        newImage.getpixel((x, y)) for x in range(fontWidth) for y in range(fontHeight)
    )
    return char, round(sum(grayscaleValues) / (fontWidth * fontHeight))


def sortByGrayscale(string: str, fontPath: str = "", fontSize: int = 14) -> list:
    """
    ### 按字符的等效灰度值排序给定字符，返回按灰度值由低到高排序好的字符列表

    参数 string: str，想要排序的字符串
    参数 fontPath: str，字体文件路径，可省略
    参数 fontSize: int，字体大小，仅在指定字体文件时生效，可省略

    返回值：lsit，已按灰度值排序好的给定字符串的字符列表
    """
    if not isinstance(string, str):
        raise TypeError("给定的参数值必须是字符串。")
    if len(string) <= 1:
        raise ValueError("空字符串或单字符无需排序。")
    grayscaleNums = [grayscaleOf(s, fontPath, fontSize) for s in string]
    grayscaleNums.sort(key=lambda x: x[1])
    return [grayscaleTuple[0] for grayscaleTuple in grayscaleNums]
