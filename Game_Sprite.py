# -*- Coding:UTF-8 -*-
"""
游戏精灵模块
"""
import sys
import pygame
import Game_Info


class WordSprite(pygame.sprite.Sprite):
    """单词精灵类"""
    def __init__(self, word_text, cn_comment, speed=1):
        super().__init__()
        self.word_text = word_text
        self.cn_comment = cn_comment
        # 创建系统字体
        self.word_font = pygame.font.SysFont(u"幼圆", Game_Info.WORD_SIZE)
        # 根据字体创建显示对象(文字)    render(self,text,antialias,color,background = None)
        self.image = self.word_font.render(word_text, True, Game_Info.GREEN_WORD)
        self.rect = self.image.get_rect()
        self.speed = speed
        pass

    def update(self):
        """垂直向下移动"""
        self.rect.y = self.rect.y + self.speed

        if self.rect.y >= Game_Info.SCREEN_RECT.height:
            print("扣分")
            self.kill()
            pass
        pass

    def __del__(self):
        print("超出屏幕%s" % self.rect)


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