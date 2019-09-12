# -*- Coding:UTF-8 -*-
"""
打字小游戏
Author:Mr Liu
Version:1.0
"""
import sys
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


if __name__ == '__main__':
    all_words = parser_words()
    typing_game = TypingGame(Game_Info.GAME_BACKGROUND)
    while True:
        for event in pygame.event.get():  # 遍历所有事件
            if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                sys.exit()

pygame.quit()