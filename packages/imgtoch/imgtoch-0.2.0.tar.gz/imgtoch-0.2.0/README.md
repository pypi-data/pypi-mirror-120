# Imgtoch

## 一个帮你将图片转为字符图片的模块。

------

### 用法：

```python
# coding: utf-8

from imgtoch import makeImage

makeImage(
    "图片路径",
    "生成的图片保存路径",
    chars = None, # 用于图像的字符表，字符数应大于 1，无需手动按名义灰度值排序
    scale = 1, # 缩放比例，0 < scale <= 1，可省略
    quality = 80, # 图片保存质量，大于 0 小于等于 100
    fontPath = "字体路径", # 可省略
    fontSize = 14, # 字体大小，仅指定字体路径时生效，可省略
    horzSep = 2, # 字符横向间隔，可省略
    vertSep = 2, # 字符纵向间隔，可省略
    keepRatio=True, # 是否保持原比例。因字体高宽不一定相等，生成的图片高宽会变形，此项为 True 则抵消变形，可省略
    keepSize=False, # 一个字符对应一个像素点，因字符有大小，所以生成的图片会比 scale 后的尺寸大，此项为 True 会将生成的图片缩放至符合 scale 后的尺寸，可省略
)
```

### 实例 1：
```python
# coding: utf-8

from imgtoch import makeImage

# 大图片尽量将 scale 设置的小些，否则生成的图片会比较大
# 字体大小 fontSize 也是影响最终生成的图片大小的因素之一
makeImage("1.jpg", "new.jpg", scale=0.2)  # 图片 1.jpg 已在当前目录中
```

### 实例 2：
```python
# coding: utf-8

from imgtoch import *

# 获取字符'#'的名义灰度值
print(grayscaleOf("#")) # ('#', 170)

# 将给定字符串按名义灰度值排序
print(sortByGrayscale("H oa.:sjv@%^a'"))
# 结果：['H', '@', 'a', '%', 'a', 's', 'j', 'o', 'v', '^', ':', "'", '.', ' ']
# 其中'a'和'%'的名义灰度值应该是相等的所以出现了'%'被夹在两个'a'中间的问题

# 更具体的参数可以看 IDE 提示或者使用 help 函数
```
