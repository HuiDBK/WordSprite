# -*- Coding:UTF-8 -*-
"""
游戏精灵模块
"""
import pygame
import Game_Info


class WordSprite(pygame.sprite.Sprite):
    """单词精灵类"""
    def __init__(self, word_text, speed=1):
        # 创建系统字体
        # self.word_font = pygame.font.sysFont(u"幼圆", 68)
        # 根据字体创建显示对象(文字)    render(self,text,antialias,color,background = None)
        self.word_surface = self.word_font.render(word_text, True, (0, 250, 0))
        self.word_rect = self.word_surface.get_rect()
        self.speed = speed
        pass

    def update(self):
        """垂直向下移动"""
        self.word_rect.y = self.word_rect.y + self.speed
        pass


class BackGroundSprite(pygame.sprite.Sprite):
    """
    背景精灵
    """
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(Game_Info.GAME_BACKGROUND)  # 加载游戏背景
        self.rect = self.image.get_rect()

    def update(self):
        pass