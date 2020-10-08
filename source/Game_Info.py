# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Hui
Description: {游戏配置信息模块}
"""
import ctypes
import pygame
import configparser


class GameConfig(object):
    """游戏配置文件类"""

    GAME_INFO = "game_info"                     # 配置文件游戏信息结点名称
    GAME_STYLE = "game_style"                   # 配置文件游戏样式结点名称
    GAME_SCORE = "game_score"                   # 配置文件游戏分数结点名称

    config_file_path = "resource/config.cfg"    # 游戏配置文件路径

    # 把配置文件类设置成单例模式
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):

        self.author = None
        self.game_name = None
        self.version = None
        self.e_mail = None

        self.frame_pre_sec = None       # 游戏帧率
        self.word_size = None           # 英文单词的大小
        self.word_normal_color = None   # 单词的正常颜色
        self.spell_ok_color = None      # 单词拼写成功的颜色
        self.game_level = None          # 游戏等级
        self.game_init_blood = None     # 游戏初始血量
        self.history_score_dict = None  # 游戏历史记录
        self.__parser_config()

    def __parser_config(self):
        """解析游戏配置文件"""
        self.conf_parser = configparser.ConfigParser()
        self.conf_parser.read(self.config_file_path, encoding='utf-8')

        # 游戏开发者信息
        self.author = self.conf_parser.get(self.GAME_INFO, 'author')
        self.game_name = self.conf_parser.get(self.GAME_INFO, 'game_name')
        self.version = self.conf_parser.get(self.GAME_INFO, 'version')
        self.e_mail = self.conf_parser.get(self.GAME_INFO, 'e-mail')

        # 游戏样式信息
        self.frame_pre_sec = self.conf_parser.get(self.GAME_STYLE, "frame_pre_sec")
        self.word_size = self.conf_parser.get(self.GAME_STYLE, "word_size")
        self.word_normal_color = self.conf_parser.get(self.GAME_STYLE, "word_normal_color")
        self.spell_ok_color = self.conf_parser.get(self.GAME_STYLE, "spell_ok_color")
        self.game_level = self.conf_parser.get(self.GAME_STYLE, "game_level")
        self.game_init_blood = self.conf_parser.get(self.GAME_STYLE, "game_init_blood")

        # {
        #   'level_0': "{'score': None,'use_time': None,'create_time': None}",
        #   'level_1': "{...}",
        #   }
        # 历史最高信息
        self.history_score_dict = dict(self.conf_parser.items(self.GAME_SCORE))

    def set_word_size(self, word_size):
        """设置单词大小"""
        self.word_size = word_size
        self.conf_parser.set(self.GAME_STYLE, "word_size", str(word_size))
        self.conf_parser.write(open(self.config_file_path, mode='w'))

    def set_game_level(self, game_level):
        """设置游戏等级"""
        self.game_level = game_level
        self.conf_parser.set(self.GAME_STYLE, "game_level", str(game_level))
        self.conf_parser.write(open(self.config_file_path, mode='w'))

    def set_game_init_blood(self, game_init_blood):
        """设置游戏的初始血条"""
        self.game_init_blood = game_init_blood
        self.conf_parser.set(self.GAME_STYLE, "game_init_blood", str(game_init_blood))
        self.conf_parser.write(open(self.config_file_path, mode='w'))

    def set_word_normal_color(self, word_normal_color):
        """设置单词的正常颜色"""
        self.word_normal_color = word_normal_color
        self.conf_parser.set(self.GAME_STYLE, "word_normal_color", str(word_normal_color))
        self.conf_parser.write(open(self.config_file_path, mode='w'))

    def set_spell_ok_color(self, spell_ok_color):
        """设置单词拼写成功后的颜色"""
        self.spell_ok_color = spell_ok_color
        self.conf_parser.set(self.GAME_STYLE, "spell_ok_color", str(spell_ok_color))
        self.conf_parser.write(open(self.config_file_path, mode='w'))

    def set_highest_score(self, score_dict, game_level):
        """更新历史最高记录"""
        self.conf_parser.set(self.GAME_SCORE, str(game_level), str(score_dict))
        self.conf_parser.write(open(self.config_file_path, mode='w'))
        self.history_score_dict = dict(self.conf_parser.items(self.GAME_SCORE))


# 获取系统屏幕分辨率(缩放比例后)
win_api = ctypes.windll.user32
SCREEN_X = win_api.GetSystemMetrics(0)
SCREEN_Y = win_api.GetSystemMetrics(1)

game_conf = GameConfig()

GAME_MUSICS = ["resource/music/bgm1.mp3", "resource/music/bgm2.mp3"]
GAME_NAME = game_conf.game_name
GAME_LEVEL = {'1': 0.3, '2': 0.5, '3': 1, '4': 1.5, '5': 2}           # 游戏困难等级与单词下落速度相互匹配字典
SCREEN_RECT = pygame.Rect(0, 0, SCREEN_X * 0.85, SCREEN_Y * 0.85)     # 游戏窗口大小(电脑分辨率 * 0.85)
INPUT_RECT_WIDTH = 600
INPUT_RECT_HEIGHT = 100
GAME_BLOOD_RECT = pygame.Rect(SCREEN_RECT.width / 2 - 250, SCREEN_RECT.height - 26, 500, 25)

GAME_ICON = "resource/image/rabbit.ico"
GAME_ICON_32 = "resource/image/rabbit_32.png"
GAME_ICON_48 = "resource/image/rabbit_48.png"
VOICE_ICO = "resource/image/voice.png"
MUTE_ICO = "resource/image/mute.png"
GAME_BACKGROUND = "resource/image/game_bg.png"
GAME_OVER_BACKGROUND = "resource/image/game_over.png"
INPUT_BACKGROUND = "resource/image/input_bg.png"
GAME_SET_BLUE = "resource/image/set_blue.png"
GAME_SET_PINK = "resource/image/set_pink.png"

GAME_FONT = "resource/font/HUI.TTF"         # 游戏字体
GAME_WORD_TEXT = "resource/en_word.txt"     # 游戏单词文本

# 单词拼写成功后的消失动画
KILL_ANIMATION = ["resource/image/animation/" + str(img_num).zfill(3) + ".png" for img_num in range(8)]

FRAME_PRE_SEC = int(game_conf.frame_pre_sec)        # 游戏的刷新帧率
WORD_SIZE = int(game_conf.word_size)                # 单词大小
WORD_FALL_SPEED = GAME_LEVEL[str(game_conf.game_level)]  # 单词下落速度
INIT_BLOOD = int(game_conf.game_init_blood)         # 游戏初始血条

# 创建单词的时间间隔(毫秒)
CREATE_WORD_INTERVAL = 1000 * 5

# 首次生成单词的数量
GENERATE_WORD_NUM = 5

# 游戏单词正常颜色和拼写颜色
WORD_NORMAL_COLOR = str(game_conf.word_normal_color)
SPELL_OK_COLOR = str(game_conf.spell_ok_color)
WORD_COLOR = pygame.color.Color(WORD_NORMAL_COLOR)
WORD_SPELL_OK_COLOR = pygame.color.Color(SPELL_OK_COLOR)

# 字体颜色
RED = pygame.color.Color("RED")
YELLOW = pygame.color.Color("YELLOW")
BLUE = pygame.color.Color("#70f3ff")
GREEN = pygame.color.Color("GREEN")
WHITE = pygame.color.Color("WHITE")
ORANGE = pygame.color.Color("ORANGE")
PINK = pygame.color.Color("#ff4777")

# 创建单词事件
CREATE_WORD_EVENT = pygame.USEREVENT
# 游戏结束事件
GAME_OVER_EVENT = pygame.USEREVENT + 1
# 游戏音乐结束事件
MUSIC_END_EVENT = pygame.USEREVENT + 2


def main():
    game_conf1 = GameConfig()
    game_conf2 = GameConfig()
    game_conf1.word_size = 100
    game_conf2.game_init_blood = 50
    print(id(game_conf1))
    print(id(game_conf2))
    print(game_conf1.game_init_blood)
    print(game_conf2.word_size)
    socre_dict = game_conf.history_score_dict
    print(dict(socre_dict))
    print(eval(socre_dict['level_1']))

    print(GAME_BLOOD_RECT)
    # print(SCREEN_X, SCREEN_Y)
    # print(SCREEN_RECT)
    # print(SCREEN_RECT.size)
    # print(game_conf.frame_pre_sec)
    # print(game_conf.game_level)
    # print(game_conf.word_size)
    # print(game_conf.word_normal_color)
    # print(game_conf.spell_ok_color)

    # print(WORD_NORMAL_COLOR)
    # print(SPELL_OK_COLOR)
    # print(int(10.000000001))
    # print(SCREEN_X, SCREEN_Y)
    # print(SCREEN_RECT.size)


if __name__ == '__main__':
    main()
