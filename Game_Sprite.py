# -*- Coding:UTF-8 -*-
"""
游戏精灵模块
Author: Mr Liu
Version: 1.0
"""
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
    """背景精灵"""

    def __init__(self, back_image):
        # 加载游戏背景
        super().__init__(back_image)

    def update(self):
        super().update()


class Bomb(object):
    # 初始化爆炸
    def __init__(self, screen):
        self.main_screen = screen
        # 加载爆炸资源
        self.images = [pygame.image.load(img) for img in Game_Info.KILL_ANIMATION]
        # 设置当前爆炸播放索引
        self.index = 0
        # 图片爆炸播放间隔
        self.interval = 3
        self.interval_index = 0
        # 爆炸位置
        self.position = [0, 0]
        # 是否可见
        self.visible = False

    # 设置爆炸播放的位置
    def set_pos(self, x, y):
        self.position[0] = x
        self.position[1] = y

    # 爆炸播放
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

    # 绘制爆炸
    def draw(self):
        # 如果对象不可见，则不绘制
        if not self.visible:
            return
        self.main_screen.screen.blit(self.images[self.index], (self.position[0], self.position[1]))


class WordSprite(pygame.sprite.Sprite):
    """单词精灵类"""
    def __init__(self, word_text, cn_comment=None, speed=Game_Info.WORD_SPEED):
        super().__init__()
        self.word_text = word_text
        self.cn_comment = cn_comment
        # 创建系统字体
        self.word_font = pygame.font.SysFont("simsunnsimsun", Game_Info.WORD_SIZE)
        # 根据字体创建显示对象(文字)    render(self,text,antialias,color,background = None)
        self.image = self.word_font.render(word_text, True, Game_Info.BLUE)
        self.rect = self.image.get_rect()
        # 用小数存储单词降落的位置
        self.y = float(self.rect.y)
        self.speed = speed
        pass

    def update(self, main_game):
        """垂直向下移动"""
        self.y += self.speed
        self.rect.y = self.y
        if main_game.score[0] >= 50:
            # 提高单词的降落速度
            self.speed = 2
        if self.rect.y >= Game_Info.SCREEN_RECT.height:
            self.kill()
            main_game.score[0] -= 1
            pass
        pass

    def set_word_color(self, word_text, color, size=Game_Info.WORD_SIZE):
        """设置文字的大小"""
        self.word_font = pygame.font.SysFont("simsunnsimsun", size)
        self.image = self.word_font.render(word_text, True, color)


class ShowTextSprite(WordSprite):
    """显示输入单词的精灵"""
    def __init__(self, display_text):
        super().__init__(display_text, speed=0)
        self.rect.x = Game_Info.SCREEN_RECT.centerx
        self.rect.y = 50

    def update(self, word_text):
        super().set_word_color(word_text, Game_Info.PINK)
        self.rect = self.image.get_rect()
        self.rect.x = Game_Info.SCREEN_RECT.width/2 - self.rect.width/2
        self.rect.y = 50


class ScoreSprite(WordSprite):
    """分数精灵"""
    def __init__(self, score):
        super().__init__(score, speed=0)
        self.rect.x = Game_Info.SCREEN_RECT.width - self.rect.width - 20
        self.rect.y = 10

    def update(self, score):
        super().set_word_color(score, Game_Info.RED, size=50)
        self.rect = self.image.get_rect()
        self.rect.x = Game_Info.SCREEN_RECT.width - self.rect.width - 20




