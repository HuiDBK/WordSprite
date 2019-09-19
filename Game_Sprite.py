# -*- Coding:UTF-8 -*-
"""
游戏精灵模块
"""
import sys
import pygame
import Game_Info


class GameSprite(pygame.sprite.Sprite):
    """游戏精灵基类"""

    def __init__(self, image, speed=0):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self, *args):
        self.rect.y = self.rect.y + self.speed
        pass


class BackGroundSprite(GameSprite):
    """
    背景精灵
    """
    def __init__(self, back_image):
        # 加载游戏背景
        super().__init__(back_image)

    def update(self):
        super().update()


class WordSprite(pygame.sprite.Sprite):
    """单词精灵类"""
    def __init__(self, word_text, cn_comment=None, speed=0.5):
        super().__init__()
        self.word_text = word_text
        self.cn_comment = cn_comment
        # 创建系统字体
        self.word_font = pygame.font.SysFont(u"幼圆", Game_Info.WORD_SIZE)
        # 根据字体创建显示对象(文字)    render(self,text,antialias,color,background = None)
        self.image = self.word_font.render(word_text, True, Game_Info.GREEN_WORD)
        self.rect = self.image.get_rect()
        # 用小数存储单词降落的位置
        self.y = float(self.rect.y)
        self.speed = speed
        pass

    def update(self):
        """垂直向下移动"""
        self.y += self.speed
        self.rect.y = self.y
        if self.rect.y >= Game_Info.SCREEN_RECT.height:
            self.kill()
            pass
        pass

    def set_word_color(self, word_text, color):
        self.image = self.word_font.render(word_text, True, color)

    def __del__(self):
        # print("超出屏幕%s" % self.rect)
        pass


class ShowTextSprite(WordSprite):
    """显示输入单词的精灵"""
    def __init__(self, display_text):
        super().__init__(display_text, speed=0)
        # 根据字体创建显示对象(文字)    render(self,text,antialias,color,background = None)
        self.image = self.word_font.render(display_text, True, Game_Info.RED_WORD)
        self.rect.x = Game_Info.SCREEN_RECT.centerx
        self.rect.y = 10

    def update(self, word_text):
        self.set_word_color(word_text)

    def set_word_color(self, word_text, color=None):
        super().set_word_color(word_text, Game_Info.RED_WORD)


