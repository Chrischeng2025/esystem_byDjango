from PIL import Image, ImageDraw, ImageFont
import random
import string
import os

from employeesystem import settings


def get_random_color():
    """生成随机颜色"""
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def generate_captcha(text, font_path=os.path.join(settings.BASE_DIR,'app01','static','font','11.ttf'), font_size=40, width=120, height=40):
    """
    生成验证码图片
    :param text: 验证码文本
    :param font_path: 字体文件路径
    :param font_size: 字体大小
    :param width: 图片宽度
    :param height: 图片高度
    :return: 验证码图片对象
    """

    # 创建图片对象
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # 加载字体
    try:
        font = ImageFont.truetype(font_path, font_size)
    except OSError:
        font = ImageFont.load_default()  # 备用默认字体

    # 绘制验证码文本
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]  # 文本宽度
    text_height = bbox[3] - bbox[1]  # 文本高度
    text_x = (width - text_width) // 2  # 水平居中
    text_y = (height - text_height) // 2  # 垂直居中
    draw.text((text_x, text_y), text, font=font, fill=get_random_color())

    # 添加一些干扰线
    for _ in range(5):
        start_pos = (random.randint(0, width), random.randint(0, height))
        end_pos = (random.randint(0, width), random.randint(0, height))
        draw.line([start_pos, end_pos], fill=get_random_color(), width=2)

    return img

