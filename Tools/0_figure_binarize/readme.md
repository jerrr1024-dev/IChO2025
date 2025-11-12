# 图片黑白二值化工具

一个简单易用的命令行图片二值化工具，支持多种二值化方法。

## 安装依赖

```bash
pip install Pillow numpy --break-system-packages
```

## 使用方法

### 基本用法

```bash
# 使用默认阈值 (127)
python binarize.py input.jpg

# 指定阈值
python binarize.py input.jpg -t 150

# 指定输出文件
python binarize.py input.jpg -o output.jpg

# 使用Otsu自动阈值法
python binarize.py input.jpg -m otsu

# 组合使用
python binarize.py input.jpg -t 100 -o output.png
```

### 参数说明

* `input`: 输入图片路径（必需）
* `-o, --output`: 输出图片路径（可选，默认为输入文件名_binary）
* `-t, --threshold`: 二值化阈值，范围0-255（可选，默认127）
* `-m, --method`: 二值化方法（可选，默认simple）
  * `simple`: 简单阈值法
  * `otsu`: Otsu自动阈值法

### 支持的图片格式

* JPG/JPEG
* PNG
* BMP
* GIF
* TIFF
* 其他PIL支持的格式

## 二值化方法说明

### 简单阈值法 (simple)

根据指定的阈值，将像素分为黑白两类：

* 像素值 > 阈值 → 白色 (255)
* 像素值 ≤ 阈值 → 黑色 (0)

适合对比度明显的图片。

### Otsu自动阈值法 (otsu)

自动计算最佳阈值，通过最大化类间方差来分离前景和背景。

适合不确定阈值的情况，效果通常更好。

## 示例

```bash
# 处理扫描文档
python binarize.py document.jpg -m otsu

# 处理低对比度图片
python binarize.py photo.png -t 100 -o photo_binary.png

# 批量处理（配合shell）
for file in *.jpg; do python binarize.py "$file" -m otsu; done
```

## 使脚本可执行（可选）

在Linux/Mac上，可以让脚本直接执行：

```bash
chmod +x binarize.py
./binarize.py input.jpg
```

在Windows上，可以创建批处理文件：

```batch
@echo off
python binarize.py %*
```

保存为 `binarize.bat`，然后可以直接使用：

```
binarize input.jpg -t 150
```
