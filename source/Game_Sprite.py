# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Hui
Description: {PyGame游戏精灵模块}
"""
import pygame
import random
import Game_Info
from Game_Info import GameConfig


class BaseSprite(pygame.sprite.Sprite):
    """游戏精灵基类"""
    def __init__(self):
        super().__init__()
        self.image = None
        self.rect = None

    def set_pos(self, x, y):
        """设置精灵位置"""
        self.rect.x = x
        self.rect.y = y

    def hor_center(self, screen_rect):
        """
        水平居中显示
        :param screen_rect: 游戏屏幕大小
        :return:
        """
        x = screen_rect.width / 2 - self.rect.width / 2
        self.set_pos(x, self.rect.y)


class ImageSprite(BaseSprite):
    """图片精灵基类"""

    def __init__(self, image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

    def transform_scale(self, image, size: tuple):
        """缩放图片大小"""
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect()


class TextSprite(BaseSprite):
    """文字精灵基类"""

    def __init__(self, text, size=Game_Info.WORD_SIZE, color=Game_Info.WHITE):
        super().__init__()
        self.text = text
        self.size = size
        self.color = color

        # 创建字体
        self.font = pygame.font.Font(Game_Info.GAME_FONT, self.size)

        # 根据字体创建显示对象(文字)    render(self,text,antialias,color,background = None)
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()

    def update(self, display_text):
        """更新显示的文字"""
        self.text = display_text
        rect_x = self.rect.x
        rect_y = self.rect.y
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y


class SpellSprite(TextSprite):
    """文字精灵基类"""

    def __init__(self, text, size=Game_Info.WORD_SIZE, color=Game_Info.WORD_SPELL_OK_COLOR):
        super().__init__(text, size, color)

    def update(self, display_text, color):
        """更新拼写的单词"""
        self.text = display_text
        self.color = color
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        # 居中显示
        self.hor_center(Game_Info.SCREEN_RECT)
        self.set_pos(self.rect.x, 40)


class WordSprite(TextSprite):
    """单词精灵类"""
    game_conf = GameConfig()

    def __init__(self, text, cn_comment, speed: float, size=28, color=Game_Info.WORD_COLOR):
        super().__init__(text, size, color)
        self.speed = speed              # 单词下落的速度
        self.cn_comment = cn_comment    # 英文单词的意思
        self.y = float(self.rect.y)     # 用小数存储单词降落的位置(方可设置成小数)

    def random_pos(self):
        """随机位置"""
        word_x = random.randint(0, Game_Info.SCREEN_RECT.width - self.rect.width)
        word_y = random.randint(-50, 10)
        self.rect.x = word_x
        self.rect.y = word_y
        self.y = float(self.rect.y)

    def update(self, game):
        """更新单词精灵"""

        # 判断游戏是否暂停
        if game.game_pause_flag:
            self.speed = 0
        else:
            self.y += self.speed
            self.rect.y = self.y

        # 超出游戏屏幕，删除精灵
        if self.rect.y >= Game_Info.SCREEN_RECT.height:
            self.kill()
            # 根据不同游戏等级掉血
            game.game_blood -= int(self.game_conf.game_level) * 3

        # 游戏配置信息改变，更新单词
        self.size = int(self.game_conf.word_size)
        self.font = pygame.font.Font(Game_Info.GAME_FONT, self.size)
        self.speed = game.game_level_dict[int(self.game_conf.game_level)]['word_fall_speed']
        self.color = pygame.color.Color(self.game_conf.word_normal_color)

        # 游戏分数是10的倍数单词下落速度提升
        if game.total_score > 0 and game.total_score % 100 == 0:
            self.speed += 0.5

        # 游戏血条在[45 - 50]区间单词下落速度提升
        if 45 * 10 <= game.game_blood <= 50 * 10:
            self.speed += 1

        # 拼写的字母与单词匹配
        if len(str(game.word_content)) >= 1 and \
                str(game.word_content)[0].lower() in str(self.text)[0].lower() and \
                str(game.word_content).lower() in str(self.text).lower():
            self.color = pygame.color.Color(self.game_conf.spell_ok_color)

        # 更新单词颜色
        self.image = self.font.render(self.text, True, self.color)


class Animation(object):
    """动画特效类"""

    def __init__(self, screen):
        """初始化动画资源"""
        self.main_screen = screen
        # 加载动画资源
        self.images = [pygame.image.load(img) for img in Game_Info.KILL_ANIMATION]
        # 设置当前动画播放索引
        self.index = 0
        # 动画播放间隔
        self.interval = 2
        self.interval_index = 0
        # 动画位置
        self.position = [0, 0]
        # 是否可见
        self.visible = False

    # 设置动画播放的位置
    def set_pos(self, x, y):
        self.position[0] = x
        self.position[1] = y

    # 动画播放
    def action(self):
        # 如果爆炸对象状态不可见，则不计算坐标
        if not self.visible:
            return

        # 控制每一帧图片的播放间隔
        self.interval_index += 1
        if self.interval_index < self.interval:
            return
        self.interval_index = 0

        self.index = self.index + 1
        if self.index >= len(self.images):
            self.index = 0
            self.visible = False

    # 绘制动画
    def draw(self):
        # 如果对象不可见，则不绘制
        if not self.visible:
            return
        self.main_screen.screen.blit(self.images[self.index], (self.position[0], self.position[1]))


def main():
    pass


if __name__ == '__main__':
    pass