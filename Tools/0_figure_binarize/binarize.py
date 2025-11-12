#!/usr/bin/env python3
"""
图片黑白二值化工具
使用方法: python binarize.py <输入图片> [选项]
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("错误: 需要安装 Pillow 库")
    print("请运行: pip install Pillow numpy --break-system-packages")
    sys.exit(1)


def binarize_image(input_path, output_path=None, threshold=127, method='simple'):
    """
    将图片二值化
    
    参数:
        input_path: 输入图片路径
        output_path: 输出图片路径（默认在原文件名后加_binary）
        threshold: 二值化阈值 (0-255，默认127)
        method: 二值化方法 ('simple' 或 'otsu')
    """
    try:
        # 读取图片
        img = Image.open(input_path)
        print(f"读取图片: {input_path}")
        print(f"图片尺寸: {img.size}, 模式: {img.mode}")
        
        # 转换为灰度图
        if img.mode != 'L':
            img = img.convert('L')
            print("已转换为灰度图")
        
        # 转换为numpy数组
        img_array = np.array(img)
        
        # 二值化处理
        if method == 'otsu':
            # Otsu自动阈值法
            threshold = otsu_threshold(img_array)
            print(f"使用Otsu方法，自动计算阈值: {threshold}")
        else:
            print(f"使用简单阈值法，阈值: {threshold}")
        
        # 应用阈值
        binary_array = (img_array > threshold) * 255
        
        # 转换回图片
        binary_img = Image.fromarray(binary_array.astype(np.uint8))
        
        # 生成输出路径
        if output_path is None:
            input_file = Path(input_path)
            output_path = input_file.parent / f"{input_file.stem}_binary{input_file.suffix}"
        
        # 保存图片
        binary_img.save(output_path)
        print(f"✓ 二值化完成，已保存到: {output_path}")
        
        return output_path
        
    except FileNotFoundError:
        print(f"错误: 找不到文件 {input_path}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)


def otsu_threshold(image_array):
    """
    使用Otsu方法自动计算最佳阈值
    """
    # 计算直方图
    histogram, _ = np.histogram(image_array, bins=256, range=(0, 256))
    histogram = histogram.astype(float)
    
    # 总像素数
    total = image_array.size
    
    # 当前最佳阈值
    current_max = 0
    threshold = 0
    
    sum_total = np.sum(np.arange(256) * histogram)
    sum_background = 0
    weight_background = 0
    
    for t in range(256):
        weight_background += histogram[t]
        if weight_background == 0:
            continue
            
        weight_foreground = total - weight_background
        if weight_foreground == 0:
            break
            
        sum_background += t * histogram[t]
        
        mean_background = sum_background / weight_background
        mean_foreground = (sum_total - sum_background) / weight_foreground
        
        # 计算类间方差
        between_class_variance = weight_background * weight_foreground * \
                                (mean_background - mean_foreground) ** 2
        
        if between_class_variance > current_max:
            current_max = between_class_variance
            threshold = t
    
    return threshold


def main():
    parser = argparse.ArgumentParser(
        description='图片黑白二值化工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  python binarize.py input.jpg                    # 使用默认阈值127
  python binarize.py input.jpg -t 150             # 指定阈值150
  python binarize.py input.jpg -o output.jpg      # 指定输出文件
  python binarize.py input.jpg -m otsu            # 使用Otsu自动阈值
  python binarize.py input.jpg -t 100 -o out.png  # 组合使用
        '''
    )
    
    parser.add_argument('input', help='输入图片路径')
    parser.add_argument('-o', '--output', help='输出图片路径（默认: 输入文件名_binary）')
    parser.add_argument('-t', '--threshold', type=int, default=127,
                       help='二值化阈值 (0-255，默认: 127)')
    parser.add_argument('-m', '--method', choices=['simple', 'otsu'], default='simple',
                       help='二值化方法 (simple: 简单阈值, otsu: 自动阈值，默认: simple)')
    
    args = parser.parse_args()
    
    # 验证阈值范围
    if not 0 <= args.threshold <= 255:
        print("错误: 阈值必须在0-255之间")
        sys.exit(1)
    
    # 执行二值化
    binarize_image(
        args.input,
        args.output,
        args.threshold,
        args.method
    )


if __name__ == '__main__':
    main()