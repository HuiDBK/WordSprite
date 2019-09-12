# -*- Coding:UTF-8 -*-
"""
游戏精灵模块
"""
import pygame
import Game_Info


class TypingGame(pygame.sprite.Sprite):
    """
    打字游戏精灵基类
    """
    def __init__(self, image_path, speed=1):
        super().__init__()
        screen = pygame.display.set_mode(Game_Info.SCREEN_SIZE)  # 设置游戏屏幕大小
        self.image = pygame.image.load(image_path)  # 加载游戏背景
        self.rect = self.image.get_rect()
        self.speed = speed
        screen.blit(self.image, self.rect)
        pygame.display.flip()

    def update(self):
        super().update(self)
        pass