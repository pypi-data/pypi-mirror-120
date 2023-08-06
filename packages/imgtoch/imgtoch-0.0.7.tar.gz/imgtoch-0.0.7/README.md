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

### 实例：
```python
# coding: utf-8

from imgtoch import makeImage

# 大图片尽量将 scale 设置的小些，否则生成的图片会比较大
# 字体大小 fontSize 也是影响最终生成的图片大小的因素之一
makeImage("1.jpg", "new.jpg", scale=0.2)  # 图片 1.jpg 已在当前目录中
```
