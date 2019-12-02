# -*- Coding:UTF-8 -*-
"""
游戏信息模块
Author: Mr Liu
Version: 1.1
"""
import configparser
import pygame


class GameConfig(object):

    # 游戏配置文件路径
    config_file_path = "config.cfg"

    def __init__(self):
        self.frame_pre_sec = None
        self.word_size = None
        self.word_normal_color = None
        self.spell_ok_color = None
        self.game_level = None
        self.game_highest_score = None
        self.game_init_blood = None
        self.__parser_config()

    def __parser_config(self):
        self.conf_parser = configparser.ConfigParser()
        self.conf_parser.read(self.config_file_path, encoding='utf-8')
        self.frame_pre_sec = self.conf_parser.get("game_style", "frame_pre_sec")
        self.word_size = self.conf_parser.get("game_style", "word_size")
        self.word_normal_color = self.conf_parser.get("game_style", "word_normal_color")
        self.spell_ok_color = self.conf_parser.get("game_style", "spell_ok_color")
        self.game_level = self.conf_parser.get("game_style", "game_level")
        self.game_init_blood = self.conf_parser.get("game_style", "game_init_blood")
        self.game_highest_score = self.conf_parser.get("score", "highest_score")

    def set_highest_score(self, highest_score):
        """修改配置文件的最高分"""
        self.conf_parser.set("score", "highest_score", str(highest_score))
        self.conf_parser.write(open(self.config_file_path, mode='w'))

    def set_word_size(self, word_size):
        """修改配置文件的单词大小"""
        self.conf_parser.set("game_style", "word_size", str(word_size))
        self.conf_parser.write(open(self.config_file_path, mode='w'))

    def set_game_level(self, game_level):
        """修改配置文件的单词大小"""
        self.conf_parser.set("game_style", "game_level", str(game_level))
        self.conf_parser.write(open(self.config_file_path, mode='w'))

    def set_game_init_blood(self, game_init_blood):
        self.conf_parser.set("game_style", "game_init_blood", str(game_init_blood))
        self.conf_parser.write(open(self.config_file_path, mode='w'))

    def set_word_normal_color(self, word_normal_color):
        self.conf_parser.set("game_style", "word_normal_color", str(word_normal_color))
        self.conf_parser.write(open(self.config_file_path, mode='w'))

    def set_spell_ok_color(self, spell_ok_color):
        self.conf_parser.set("game_style", "spell_ok_color", str(spell_ok_color))
        self.conf_parser.write(open(self.config_file_path, mode='w'))


game_conf = GameConfig()

GAME_MUSICS = ["image/卡农.mp3", "image/龙珠.mp3"]
GAME_NAME = "WordSprite"
GAME_LEVEL = {'1': 0.3, '2': 0.5, '3': 0.8, '4': 1.3, '5': 1.8}     # 游戏困难等级与单词下落速度相互匹配
SCREEN_RECT = pygame.Rect(0, 0, 1200, 800)
INPUT_RECT_WIDTH = 600
INPUT_RECT_HEIGHT = 100
GAME_BLOOD_RECT = pygame.Rect(SCREEN_RECT.width / 2 - 250, SCREEN_RECT.height - 26, 500, 25)

GAME_ICON = "image/rabbit.ico"
GAME_BACKGROUND = "image/game_bg.png"
GAME_OVER_BACKGROUND = "image/game_over.png"
INPUT_BACKGROUND = "image/input_bg.png"
GAME_SET_BLUE = "image/set_blue.png"
GAME_SET_PINK = "image/set_pink.png"
SCORE_RECORD_FILE = "score_record.txt"


# 单词拼写成功后的消失动画
KILL_ANIMATION = ["image/000.png", "image/001.png", "image/002.png", "image/003.png", "image/004.png",
                  "image/005.png", "image/006.png", "image/007.png"]

FRAME_PRE_SEC = int(game_conf.frame_pre_sec)  # 游戏的刷新帧率
WORD_SIZE = int(game_conf.word_size)      # 单词大小
WORD_SPEED = GAME_LEVEL[str(game_conf.game_level)]   # 单词下落速度
INIT_BLOOD = int(game_conf.game_init_blood)     # 游戏初始血条

# 创建单词的时间间隔(毫秒)
CREATE_WORD_INTERVAL = 1000 * 5

# 首次生成单词的数量
GENERATE_WORD_NUM = 6

# 游戏单词正常颜色和拼写颜色
WORD_NORMAL_COLOR = str(game_conf.word_normal_color)
SPELL_OK_COLOR = str(game_conf.spell_ok_color)

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
    # game_conf = GameConfig()
    # print(game_conf.frame_pre_sec)
    # print(game_conf.game_level)
    # print(game_conf.word_size)
    # print(game_conf.word_normal_color)
    # print(game_conf.spell_ok_color)

    # print(WORD_NORMAL_COLOR)
    # print(SPELL_OK_COLOR)
    print(int(10.000000001))


if __name__ == '__main__':
    main()