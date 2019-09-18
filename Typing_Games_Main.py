# -*- Coding:UTF-8 -*-
"""
打字小游戏
Author:Mr Liu
Version:1.0
"""
import sys
import pygame
from Game_Sprite import *

pygame.init()


def parser_words():
    """
    解析英语单词
    :return english_words
    """
    english_words = []
    word_contents = open("english_word.txt", encoding="gbk")
    for value in word_contents:
        value = value.lstrip()
        word_list = value.split(" ")
        words = [i for i in word_list if i != '']
        if len(words) >= 2:
            english_words.append({words[0]: words[1]})
    return english_words


class TypingGame(object):
    """打字游戏主类"""
    def __init__(self):
        self.screen = pygame.display.set_mode(Game_Info.SCREEN_SIZE)
        self.game_clock = pygame.time.Clock()
        self.__create_sprite()
        pass

    def __create_sprite(self):
        """创建精灵"""
        back_sprite = BackGroundSprite()
        word_sprite = WordSprite("hui")
        self.back_group = pygame.sprite.Group(back_sprite)
        self.word_group = pygame.sprite.Group(word_sprite)
        pass

    def __update_sprite(self):
        """更新精灵"""
        self.back_group.update()
        self.word_group.update()
        # 把背景精灵组中的所有精灵绘制到游戏屏幕上
        self.back_group.draw(self.screen)
        self.word_group.draw(self.screen)
        pygame.display.update()     # 最后更新游戏屏幕
        pass

    def start_game(self):
        """打字游戏开启"""
        while True:
            # 设置游戏刷新帧率
            self.game_clock.tick(Game_Info.FRAME_PRE_SEC)
            self.__update_sprite()
        pass

    def __event_handle(self):
        """事件监听"""
        for event in pygame.event.get():  # 遍历所有事件
            if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                sys.exit()
        pass

    def __check_collide(self):
        """检查越界"""
        pass


if __name__ == '__main__':
    typing_game = TypingGame()
    typing_game.start_game()
    pygame.quit()