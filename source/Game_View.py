# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Hui
Description: {游戏视图模块}
"""
import Game_Info
import threading
import PySimpleGUI as sg
from Game_Info import GameConfig
from tkinter import colorchooser
from Game_Main import TypingGame


class BaseWin(object):
    """窗口父类"""
    WIN_THEME = sg.theme('DarkBlue1')
    text_color = 'white'
    game_conf = GameConfig()    # 游戏信息配置类

    def __init__(self, title):
        self.title = title
        self.window = None
        self.layout = list()

    def close_win(self):
        """关闭窗口"""
        if self.window is not None:
            self.window.close()


class GameStartWin(BaseWin):
    """游戏开始窗口"""
    _voice_flag = True

    def __init__(self, title):
        super().__init__(title)
        self.__init_layout()

    def __init_layout(self):
        """初始化窗口布局"""
        if self._voice_flag:
            voice_img = Game_Info.VOICE_ICO
        else:
            voice_img = Game_Info.MUTE_ICO
        self.layout = [
            [sg.Text(size=(70, 0)), sg.Image(filename=voice_img, key='voice_control', enable_events=True)],
            [sg.Text(size=(10, 10)), sg.Text('Word  Sprite', font=(u'宋体', 50)), sg.Text(size=(10, 10))],
            [sg.Text(size=(23, 10)), sg.Button(u'开始游戏', font=(u'宋体', 30), key='start_game'), sg.Text(size=(23, 10))],
            [sg.Text(size=(23, 5)), sg.Button(u'游戏设置', font=(u'宋体', 30), key='game_set'), sg.Text(size=(23, 5))],
            [sg.Text(size=(23, 10)), sg.Button(u'历史最高', font=(u'宋体', 30), key='show_score'), sg.Text(size=(23, 10))],
            [
                sg.Text(size=(70, 0)),
                sg.Image(
                    filename=Game_Info.GAME_ICON_48,
                    key='game_ico',
                    enable_events=True
                )
             ]
        ]

    def run(self):
        """启动游戏开始窗口"""
        self.window = sg.Window(
            title=self.title,
            icon=Game_Info.GAME_ICON,
            layout=self.layout
        )
        self.__event_handler()

    def __event_handler(self):
        """窗口事件监听"""
        while True:
            event, value_dict = self.window.read(timeout=20)
            print(event, value_dict)

            # 静音控制
            if self._voice_flag:
                self.window.find_element('voice_control').update(filename=Game_Info.VOICE_ICO)
            else:
                self.window.find_element('voice_control').update(filename=Game_Info.MUTE_ICO)

            if event in (sg.WIN_CLOSED, 'Quit'):
                break
            elif event in 'voice_control':
                self.voice_control()
            elif event in 'game_ico':
                self.author_win()
            elif event in 'start_game':
                print('开始游戏')
                self.window.Hide()
                TypingGame.game_over_flag = False
                TypingGame.game_quit_flag = False
                threading.Thread(target=self.start_game).start()    # 利用线程开启游戏防止窗口卡死
            elif event in 'game_set' or TypingGame.game_pause_flag:
                print('游戏设置')
                self.window.Disable()
                self.game_set()
            elif event in 'show_score':
                print('历史最高')
                self.window.Disable()
                self.show_score()
            elif TypingGame.game_quit_flag:
                self.window.UnHide()
        self.window.close()

    def voice_control(self):
        """游戏静音状态控制"""
        if self._voice_flag:
            GameStartWin._voice_flag = False
            self.window.find_element('voice_control').update(filename=Game_Info.MUTE_ICO)
        else:
            GameStartWin._voice_flag = True
            self.window.find_element('voice_control').update(filename=Game_Info.VOICE_ICO)

    def author_win(self):
        """游戏开发信息窗口"""
        self.window.Disable()
        game_conf = Game_Info.GameConfig()

        show_text = '游戏作者: \t' + game_conf.author + '\n\n'\
                    '游戏名称: \t' + game_conf.game_name + '\n\n'\
                    '游戏版本: \t' + game_conf.version + '\n\n'\
                    '作者邮箱: \t' + game_conf.e_mail + '\n'
        sg.Popup(
            show_text,
            title=u'关于作者',
            icon=Game_Info.GAME_ICON,
            font=(u'宋体', 18),
            custom_text=(u'  ★  ', u'  ❤  '),
            button_color=('red', '#063288'),
            line_width=50,
        )
        self.window.Enable()

    def game_set(self):
        """游戏设置"""
        GameSetWin(u"游戏配置", self).run()

    def show_score(self):
        """查看历史最高分"""
        GameScoreWin(u'历史最高', self).run()

    @staticmethod
    def start_game():
        """开始游戏"""
        TypingGame().start_game()

    @classmethod
    def voice_flag(cls):
        return cls._voice_flag


class GameExecuteWin(object):
    """游戏运行窗口"""
    pass


class GameEndWin(object):
    """游戏结束窗口"""

    def __init__(self):
        pass


class GameSetWin(BaseWin):
    """游戏配置信息窗口"""

    # 游戏等级对照字典
    game_level_dict = {
        1: {"game_level_num": 5, "game_level_text": u"简单", "game_level_color": "green"},
        2: {"game_level_num": 15, "game_level_text": u"上手", "game_level_color": "blue"},
        3: {"game_level_num": 25, "game_level_text": u"中等", "game_level_color": "orange"},
        4: {"game_level_num": 35, "game_level_text": u"困难", "game_level_color": "red"},
        5: {"game_level_num": 50, "game_level_text": u"魔鬼", "game_level_color": "purple"}
    }

    def __init__(self, title, parent_win=None):
        """初始化游戏配置界面"""
        super().__init__(title)
        self.parent_win = parent_win
        self.word_normal_color = self.game_conf.word_normal_color
        self.spell_ok_color = self.game_conf.spell_ok_color
        self.__init_layout()+

    def __init_layout(self):
        game_level_num = self.game_level_dict[int(self.game_conf.game_level)]["game_level_num"]
        game_level_text = self.game_level_dict[int(self.game_conf.game_level)]["game_level_text"]
        game_level_color = self.game_level_dict[int(self.game_conf.game_level)]["game_level_color"]

        self.layout = [
            [
                sg.Text(u'游戏难度等级:', text_color=self.text_color),
                sg.Slider(
                    range=(1, 50), default_value=game_level_num,
                    size=(26, 18), orientation='h', key="game_level",
                    enable_events=True, disable_number_display=True,
                ),
                sg.Button(
                    game_level_text, key='game_level_btn',
                    button_color=(self.text_color, game_level_color),
                ),
            ],
            [
                sg.Text(u'游戏字体大小:', text_color=self.text_color),
                sg.Slider(
                    range=(15, 35), default_value=int(self.game_conf.word_size),
                    size=(26, 18), enable_events=True,
                    orientation='h', disable_number_display=True, key="word_size"
                ),
                sg.Text(
                    str(self.game_conf.word_size), text_color=self.text_color, size=(3, 1),
                    font=("宋体", int(self.game_conf.word_size)),
                    key='word_size_num'
                ),
            ],
            [
                sg.Text(u'游戏初始血条:', text_color=self.text_color),
                sg.Slider(
                    range=(5, 30), default_value=int(self.game_conf.game_init_blood),
                    size=(26, 18), orientation='h',
                    enable_events=True, disable_number_display=True, key='init_blood'
                ),
                sg.Text(
                    str(self.game_conf.game_init_blood), size=(3, 1),
                    text_color=self.text_color, key='blood_num'
                )
            ],
            [
                sg.Text(u'游戏静音状态:', text_color=self.text_color),
                sg.Radio(
                    ' ', default=GameStartWin.voice_flag(), key='voice_open',
                    group_id=1, text_color=self.text_color, enable_events=True
                ),
                sg.Image(filename=Game_Info.VOICE_ICO),
                sg.Text(' ' * 5),
                sg.Radio(
                    ' ', default=not GameStartWin.voice_flag(), key='mute',
                    group_id=1, text_color=self.text_color, enable_events=True
                ),
                sg.Image(filename=Game_Info.MUTE_ICO)
            ],
            [
                sg.Text(u'游戏字体颜色:', text_color=self.text_color),
                sg.Text(
                    '', size=(17, 1),
                    background_color=self.game_conf.word_normal_color,
                    enable_events=True, key='word_normal_color'
                ),
                sg.Text(
                    'HUI', key='word_color_test',
                    text_color=self.game_conf.word_normal_color,
                ),
                sg.Button(u'颜色选择', key='normal_ccb')
            ],
            [
                sg.Text(u'单词拼写颜色:', text_color=self.text_color),
                sg.Text(
                    '', size=(17, 1),
                    background_color=self.game_conf.spell_ok_color,
                    enable_events=True, key='spell_ok_color'
                ),
                sg.Text(
                    'HUI', key='spell_color_test',
                    text_color=self.game_conf.spell_ok_color,
                ),
                sg.Button(u'颜色选择', key='spell_ccb')
            ],
            [
                sg.Submit(u'暂时保存', key='temp_save', pad=((10, 350), (0, 0))),
                sg.Button(u'永久保存', key='permanent')
            ]
        ]

    def run(self):
        """开启游戏设置界面"""
        self.window = sg.Window(
            title=self.title,
            icon=Game_Info.GAME_ICON,
            layout=self.layout,
            font=("宋体", 18),
            element_padding=(10, 30),
        )
        # 开启事件监听
        self.__event_handler()

    @staticmethod
    def color_callback(color=None):
        """颜色按钮回调方法"""
        return colorchooser.askcolor(color)

    def __event_handler(self):
        while True:
            event, value_dict = self.window.read()
            # print(event, value_dict)
            if event in (None, 'Quit'):
                break
            elif event in ('voice_open', 'mute'):
                if value_dict['voice_open']:
                    GameStartWin._voice_flag = True
                else:
                    GameStartWin._voice_flag = False
            elif event in 'game_level':
                game_level = self.get_game_level(int(value_dict[event]))
                game_level_text = self.game_level_dict[game_level]['game_level_text']
                game_level_color = self.game_level_dict[game_level]['game_level_color']
                self.window.find_element('game_level_btn').update(
                    game_level_text,
                    button_color=(self.text_color, game_level_color)
                )
            elif event in 'game_level_btn':
                # 点击按钮切换游戏等级
                game_level = self.get_game_level(int(value_dict['game_level']))
                if game_level == 5:
                    game_level = 0
                game_level_num = self.game_level_dict[game_level + 1]['game_level_num']
                game_level_text = self.game_level_dict[game_level + 1]['game_level_text']
                game_level_color = self.game_level_dict[game_level + 1]['game_level_color']

                self.window.find_element('game_level').update(game_level_num)
                self.window.find_element('game_level_btn').update(
                    game_level_text,
                    button_color=(self.text_color, game_level_color)
                )
            elif event in 'word_size':
                word_size_num = value_dict[event]
                self.window.find_element('word_size_num').update(int(word_size_num), font=(u'宋体', int(word_size_num)))
            elif event in 'init_blood':
                blood_num = int(value_dict[event])
                self.window.find_element('blood_num').update(str(blood_num))
            elif event in 'normal_ccb':
                # 游戏单词颜色选择
                self.window.Disable()  # 让游戏配置窗口不可用，不让用户乱点击，防止多开
                choose_colors = self.color_callback(self.game_conf.word_normal_color)
                self.window.Enable()  # 恢复游戏配置窗口
                if None not in choose_colors:
                    self.window.find_element('word_normal_color').update(background_color=choose_colors[1])
                    self.window.find_element('word_color_test').update(text_color=choose_colors[1])
                    self.word_normal_color = choose_colors[1]
            elif event in 'spell_ccb':
                # 单词拼写颜色选择
                self.window.Disable()  # 让游戏配置窗口不可用，不让用户乱点击，防止多开
                choose_colors = self.color_callback(self.game_conf.spell_ok_color)
                self.window.Enable()  # 恢复游戏配置窗口
                if None not in choose_colors:
                    self.window.find_element('spell_ok_color').update(background_color=choose_colors[1])
                    self.window.find_element('spell_color_test').update(text_color=choose_colors[1])
                    self.spell_ok_color = choose_colors[1]
            elif event in ('temp_save', 'permanent'):
                GameSetWin.SAVE_STATUS = True
                game_level = self.get_game_level(int(value_dict['game_level']))
                value_dict['game_level'] = game_level
                value_dict['normal_ccb'] = self.word_normal_color
                value_dict['spell_ccb'] = self.spell_ok_color
                if event in 'temp_save':
                    self.temp_save(value_dict)
                elif event in 'permanent':
                    self.permanent(value_dict)
                break

        self.window.close()
        TypingGame.game_pause_flag = False

        # 恢复父窗口可用
        if self.parent_win is not None:
            self.parent_win.window.Enable()

    def temp_save(self, game_dict):
        """临时保存游戏配置信息(临时有效，重开还原)"""
        """
               {
                   'game_level': 2, 
                   'word_size': 26.0, 
                   'init_blood': 20.0, 
                   'voice_open': True, 
                   'mute': False,
                   'normal_ccb': '#00ffff', 
                   'spell_ccb': '#ff0000'
               }
        """
        self.game_conf.game_level = game_dict['game_level']
        self.game_conf.word_size = game_dict['word_size']
        self.game_conf.game_init_blood = game_dict['init_blood']
        self.game_conf.word_normal_color = game_dict['normal_ccb']
        self.game_conf.spell_ok_color = game_dict['spell_ccb']

    def permanent(self, game_dict):
        """永久保存游戏配置信息(写入配置文件)"""

        # 修改配置文件
        self.game_conf.set_game_level(game_dict['game_level'])
        self.game_conf.set_word_size(int(game_dict['word_size']))
        self.game_conf.set_game_init_blood(int(game_dict['init_blood']))
        self.game_conf.set_word_normal_color(game_dict['normal_ccb'])
        self.game_conf.set_spell_ok_color(game_dict['spell_ccb'])

    @staticmethod
    def get_game_level(data):
        game_level = 1
        if data <= 10:
            game_level = 1
        elif data <= 20:
            game_level = 2
        elif data <= 30:
            game_level = 3
        elif data <= 40:
            game_level = 4
        elif data <= 50:
            game_level = 5
        return game_level#


class GameScoreWin(BaseWin):
    """游戏历史分数窗口"""
    heads = [
        '{:4}'.format(u'游戏等级'),
        '{:4}'.format(u'最高分'),
        '{:6}'.format(u'耗 时'),
        '{:4}'.format(u'创建时间'),
    ]
    levels = ['level_1', 'level_2', 'level_3', 'level_4', 'level_5']

    def __init__(self, title, parent_win=None):
        super().__init__(title)
        self.parent_win = parent_win
        self.__init_layout()

    def __init_layout(self):
        """初始化窗口布局"""
        score_dict = Game_Info.game_conf.history_score_dict       # 游戏历史记录
        level_0, level_1 = eval(score_dict[self.levels[0]]), eval(score_dict[self.levels[1]])
        level_2, level_3 = eval(score_dict[self.levels[2]]), eval(score_dict[self.levels[3]])
        level_4 = eval(score_dict[self.levels[4]])

        header = [[sg.Text(h, pad=(31, 30)) for h in self.heads]]
        body = [
            [
                sg.Button(u'简单', button_color=('white', 'green')),
                sg.Text('{:4}'.format(str(level_0['score']))),
                sg.Text('{:6}'.format(str(level_0['use_time']))),
                sg.Text('{:4}'.format(str(level_0['create_time'])))
            ],
            [
                sg.Button(u'上手', button_color=('white', 'blue')),
                sg.Text('{:4}'.format(str(level_1['score']))),
                sg.Text('{:6}'.format(str(level_1['use_time']))),
                sg.Text('{:4}'.format(str(level_1['create_time'])))
            ],
            [
                sg.Button(u'中等', button_color=('white', 'orange')),
                sg.Text('{:4}'.format(str(level_2['score']))),
                sg.Text('{:6}'.format(str(level_2['use_time']))),
                sg.Text('{:4}'.format(str(level_2['create_time'])))
            ],
            [
                sg.Button(u'困难', button_color=('white', 'red')),
                sg.Text('{:4}'.format(str(level_3['score']))),
                sg.Text('{:6}'.format(str(level_3['use_time']))),
                sg.Text('{:4}'.format(str(level_3['create_time'])))
            ],
            [
                sg.Button(u'魔鬼', button_color=('white', 'purple')),
                sg.Text('{:4}'.format(str(level_4['score']))),
                sg.Text('{:6}'.format(str(level_4['use_time']))),
                sg.Text('{:4}'.format(str(level_4['create_time'])))
            ]
        ]
        self.layout = header + body

    def run(self):
        """启动游戏历史分数窗口"""
        self.window = sg.Window(
            title=self.title,
            icon=Game_Info.GAME_ICON,
            layout=self.layout,
            font=('宋体', 20),
            element_padding=(46, 30)
        )
        self.__event_handler()

    def __event_handler(self):
        """窗口事件监听"""
        while True:
            event, value_dict = self.window.read()
            print(event, value_dict)
            if event in (sg.WIN_CLOSED, 'Quit'):
                self.parent_win.window.Enable()
                break
        self.window.close()


def main():
    GameStartWin(title="Word Sprite").run()


if __name__ == '__main__':
    main()