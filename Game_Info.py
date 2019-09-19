# -*- Coding:UTF-8 -*-
"""
游戏信息模块
"""
import pygame

GAME_NAME = "WordSprite"
SCREEN_RECT = pygame.Rect(0, 0, 1000, 650)
GAME_BACKGROUND = "image/game_bg.jpg"
WHITE_RECT = "image/white_rect.png"
FRAME_PRE_SEC = 60      # 游戏的刷新帧率
WORD_SIZE = 25          # 单词大小

# 字体颜色
RED_WORD = pygame.color.Color("RED")
YELLOW_WORD = pygame.color.Color("YELLOW")
BLUE_WORD = pygame.color.Color("BLUE")
GREEN_WORD = pygame.color.Color("GREEN")
WHITE_WORD = pygame.color.Color("WHITE")

# 创建单词的时间间隔(毫秒)
CREATE_WORD_INTERVAL = 1000 * 2
GENERATE_WORD_NUM = 6   # 首次生成单词的数量

# 创建单词事件
CREATE_WORD_EVENT = pygame.USEREVENT
# 游戏结束事件
GAME_OVER_EVENT = pygame.USEREVENT + 1

if __name__ == '__main__':
    a = "456abc"
    print(a[:-1])