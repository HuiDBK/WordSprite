# -*- Coding:UTF-8 -*-
"""
打字小游戏
Author: Mr Liu
Version: 1.1
"""

import os
import sys
import random
import traceback
import colorsys
import multiprocessing

import pyautogui as gui
import PySimpleGUI as sg
from Game_Sprite import *

pygame.init()


def random_music():
    """随机播放音乐"""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(random.choice(Game_Info.GAME_MUSICS))
        pygame.mixer.music.play(loops=0)
    except Exception:
        print("无法加载音频，请检查电脑配置")
        print(traceback.format_exc())


# 获取电脑屏幕分辨率
screen_width, screen_height = gui.size()
game_x = (screen_width - Game_Info.SCREEN_RECT.width) / 2
game_y = (screen_height - Game_Info.SCREEN_RECT.height) / 2
# 设置游戏窗口相对电脑屏幕居中
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (game_x, game_y)


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
            # 把解析好的单词和注释封装到字典中，然后加入列表
            english_words.append(
                {"eng_word": words[0], "cn_comment": words[1]})
    return english_words


def start_game_set_win(game_queue, game_info_dict):
    """开启游戏配置窗口"""
    GameSetWin(u"游戏配置", game_queue, game_info_dict).start()


class GameSetWin(object):
    """游戏配置窗口"""

    bg_color = '#415569'  # 窗口背景颜色
    text_color = 'white'

    game_level_dict = {
        1: {"game_level_num": 5, "game_level_text": u"简单", "game_level_color": "green"},
        2: {"game_level_num": 15, "game_level_text": u"上手", "game_level_color": "blue"},
        3: {"game_level_num": 25, "game_level_text": u"中等", "game_level_color": "orange"},
        4: {"game_level_num": 35, "game_level_text": u"困难", "game_level_color": "red"},
        5: {"game_level_num": 50, "game_level_text": u"魔鬼", "game_level_color": "purple"}
    }

    def __init__(self, title, game_queue, Game_Info):
        """初始化游戏配置界面"""
        self.title = title
        self.game_queue = game_queue
        self.Game_Info = Game_Info
        self.window = None
        self.__init_layout()

    def __init_layout(self):
        game_level_num = self.game_level_dict[int(self.Game_Info['GAME_LEVEL'])]["game_level_num"]
        game_level_text = self.game_level_dict[int(self.Game_Info['GAME_LEVEL'])]["game_level_text"]
        game_level_color = self.game_level_dict[int(self.Game_Info['GAME_LEVEL'])]["game_level_color"]
        # if int(Game_Info.game_conf.game_level) == 1:
        #     game_level_num = 5
        #     game_level_text = u'简单'
        #     game_level_color = 'green'
        # elif int(Game_Info.game_conf.game_level) == 2:
        #     game_level_num = 15
        #     game_level_text = u'上手'
        #     game_level_color = 'blue'
        # elif int(Game_Info.game_conf.game_level) == 3:
        #     game_level_num = 25
        #     game_level_text = u'中等'
        #     game_level_color = 'orange'
        # elif int(Game_Info.game_conf.game_level) == 4:
        #     game_level_num = 35
        #     game_level_text = u'困难'
        #     game_level_color = 'red'
        # elif int(Game_Info.game_conf.game_level) == 5:
        #     game_level_num = 50
        #     game_level_text = u'魔鬼'
        #     game_level_color = 'purple'
        self.layout = [
            [
                sg.Text(u'游戏难度等级:', text_color=self.text_color, background_color=self.bg_color),
                sg.Slider(range=(1, 50), default_value=game_level_num, size=(26, 18), orientation='h',
                          enable_events=True, disable_number_display=True, background_color=self.bg_color,
                          key="game_level"),
                sg.Button(game_level_text, button_color=(self.text_color, game_level_color), key='game_level_btn')
            ],
            [
                sg.Text(u'游戏字体大小:', text_color=self.text_color, background_color=self.bg_color),
                sg.Slider(range=(15, 35), default_value=self.Game_Info['WORD_SIZE'], size=(26, 18),
                          enable_events=True, orientation='h', disable_number_display=True,
                          background_color=self.bg_color, key="word_size"),
                sg.Text(self.Game_Info['WORD_SIZE'], text_color=self.text_color,
                        background_color=self.bg_color, key='word_size_num')
            ],
            [
                sg.Text(u'游戏初始血条:', text_color=self.text_color, background_color=self.bg_color),
                sg.Slider(range=(5, 30), default_value=self.Game_Info['INIT_BLOOD'], size=(26, 18), orientation='h',
                          enable_events=True, disable_number_display=True, background_color=self.bg_color,
                          key='init_blood'),
                sg.Text(str(self.Game_Info['INIT_BLOOD']), text_color=self.text_color,
                        background_color=self.bg_color, key='blood_num')
            ],
            [
                sg.Text(u'游戏字体颜色:', text_color=self.text_color, background_color=self.bg_color),
                sg.Text('', size=(17, 1), background_color=self.Game_Info['WORD_NORMAL_COLOR'],
                        key='word_normal_color'),
                sg.ColorChooserButton(u'颜色选择', key='normal_ccb')
            ],
            [
                sg.Text(u'单词拼写颜色:', text_color=self.text_color, background_color=self.bg_color),
                sg.Text('', size=(17, 1), background_color=self.Game_Info['SPELL_OK_COLOR'],
                        key='spell_ok_color'),
                sg.ColorChooserButton(u'颜色选择', key='spell_ccb')
            ],
            [
                sg.Submit(u'暂时保存', key='temp_save', pad=((10, 350), (0, 0))),
                sg.Button(u'永久保存', key='permanent')
            ]
        ]

    def start(self):
        """开启游戏配置界面"""
        self.window = sg.Window(title=self.title, layout=self.layout, element_padding=(10, 30),
                                font=('宋体', 18), background_color=self.bg_color, keep_on_top=True)
        # 开启事件监听
        self.__event_handler()

    def __event_handler(self):
        while True:
            event, value_dict = self.window.read(timeout=10)
            print(event, value_dict)
            if event in (None, 'Quit'):
                self.game_queue.put({"result": "quit", "type": 'quit'})
                break
            elif event in 'game_level':
                game_level = self.get_game_level(int(value_dict[event]))
                game_level_text = self.game_level_dict[game_level]['game_level_text']
                game_level_color = self.game_level_dict[game_level]['game_level_color']
                self.window.find_element('game_level_btn').update(game_level_text, button_color=(self.text_color, game_level_color))
                # if int(game_level_num) <= 10:
                #     self.window.find_element('game_level_btn').update(u'简单', button_color=(self.text_color, 'green'))
                # elif int(game_level_num) <= 20:
                #     self.window.find_element('game_level_btn').update(u'上手', button_color=(self.text_color, 'blue'))
                # elif int(game_level_num) <= 30:
                #     self.window.find_element('game_level_btn').update(u'中等', button_color=(self.text_color, 'orange'))
                # elif int(game_level_num) <= 40:
                #     self.window.find_element('game_level_btn').update(u'困难', button_color=(self.text_color, 'red'))
                # elif int(game_level_num) <= 50:
                #     self.window.find_element('game_level_btn').update(u'魔鬼', button_color=(self.text_color, 'purple'))
            elif event in 'game_level_btn':
                # 点击按钮切换游戏等级
                game_level = self.get_game_level(int(value_dict['game_level']))
                if game_level == 5:
                    game_level = 0
                game_level_num = self.game_level_dict[game_level+1]['game_level_num']
                game_level_text = self.game_level_dict[game_level+1]['game_level_text']
                game_level_color = self.game_level_dict[game_level+1]['game_level_color']

                self.window.find_element('game_level').update(game_level_num)
                self.window.find_element('game_level_btn').update(game_level_text, button_color=(self.text_color, game_level_color))

                # if int(game_level_num) <= 10:
                #     self.window.find_element('game_level').update(15)
                #     self.window.find_element('game_level_btn').update(u'上手', button_color=(self.text_color, 'blue'))
                # elif int(game_level_num) <= 20:
                #     self.window.find_element('game_level').update(25)
                #     self.window.find_element('game_level_btn').update(u'中等', button_color=(self.text_color, 'orange'))
                # elif int(game_level_num) <= 30:
                #     self.window.find_element('game_level').update(35)
                #     self.window.find_element('game_level_btn').update(u'困难', button_color=(self.text_color, 'red'))
                # elif int(game_level_num) <= 40:
                #     self.window.find_element('game_level').update(50)
                #     self.window.find_element('game_level_btn').update(u'魔鬼', button_color=(self.text_color, 'purple'))
                # elif int(game_level_num) <= 50:
                #     self.window.find_element('game_level').update(5)
                #     self.window.find_element('game_level_btn').update(u'简单', button_color=(self.text_color, 'green'))
            elif event in 'word_size':
                word_size_num = value_dict[event]
                self.window.find_element('word_size_num').update(word_size_num)
            elif event in 'init_blood':
                blood_num = int(value_dict[event])
                self.window.find_element('blood_num').update(str(blood_num))
            elif event in 'temp_save':
                game_level = self.get_game_level(int(value_dict['game_level']))
                value_dict['game_level'] = game_level
                self.game_queue.put({"result": value_dict, "type": 'temp_save'})
                break
            elif event in 'permanent':
                game_level = self.get_game_level(int(value_dict['game_level']))
                value_dict['game_level'] = game_level
                self.game_queue.put({"result": value_dict, "type": 'permanent'})
                break
            # 颜色选择
            if value_dict['normal_ccb']:
                normal_word_color = value_dict['normal_ccb']
                self.window.find_element('word_normal_color').update(background_color=normal_word_color)
            if value_dict['spell_ccb']:
                spell_ok_color = value_dict['spell_ccb']
                self.window.find_element('spell_ok_color').update(background_color=spell_ok_color)
        self.window.close()
        sg.quit()
        multiprocessing.current_process().close()

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
        return game_level


class TypingGame(object):
    """打字游戏主类"""

    # 用于标识单词拼写成功
    spell_ok = False
    game_pause_flag = False  # 游戏暂停标志
    game_over_flag = False  # 游戏结束标志
    game_queue = multiprocessing.Queue()  # 创建游戏队列，方便在进程中通信

    def __init__(self):
        self.words = parser_words()
        self.screen = pygame.display.set_mode(Game_Info.SCREEN_RECT.size)
        # 预先创建爆炸对象
        self.bombs = [Bomb(self) for _ in range(5)]
        self.game_clock = pygame.time.Clock()
        self.__create_sprite()
        self.total_score = 0  # 记录游戏拼写成功了多少个单词
        self.game_blood = Game_Info.INIT_BLOOD  # 游戏初始血条值
        self.word_content = ""
        self.backspace_state = False  # 按下状态
        self.backspace_count = 0
        # 绘制游戏能量
        self.__draw_game_blood()
        # 设置创建单词的定时器
        pygame.time.set_timer(Game_Info.CREATE_WORD_EVENT,
                              Game_Info.CREATE_WORD_INTERVAL)
        # 设置游戏音乐结束事件
        try:
            pygame.mixer.music.set_endevent(Game_Info.MUSIC_END_EVENT)
        except Exception as e:
            print("无法设置音乐结束事件\t" + str(e))
            # 打印异常行数
            print(str(e.__traceback__.tb_lineno))
        # 设置游戏标题和图标
        pygame.display.set_caption(Game_Info.GAME_NAME)
        pygame.display.set_icon(pygame.image.load(Game_Info.GAME_ICON))

    def __create_sprite(self):
        """创建精灵和精灵组"""

        # 背景精灵
        back_sprite = BackGroundSprite(Game_Info.GAME_BACKGROUND)
        self.back_group = pygame.sprite.Group(back_sprite)

        # 游戏结束精灵组
        self.game_over_group = pygame.sprite.Group()
        game_over_sprite = TextSprite("Game  Over")
        game_over_sprite.size = 100
        self.game_over_x = (Game_Info.SCREEN_RECT.width - game_over_sprite.rect.width) / 2
        self.game_over_y = (Game_Info.SCREEN_RECT.height - game_over_sprite.rect.height - 200) / 2
        game_over_sprite.set_pos(self.game_over_x, self.game_over_y)

        self.highest_sprite = TextSprite("")
        self.highest_sprite.size = 50

        self.ok_sprite = TextSprite(u"确 定")
        self.ok_sprite.size = 50
        self.ok_sprite.set_pos(self.game_over_x - 100, self.game_over_y + 250)

        self.reset_sprite = TextSprite(u"重 玩")
        self.reset_sprite.size = 50
        self.reset_sprite.set_pos(game_over_sprite.rect.x + game_over_sprite.rect.width - 50,
                                  self.game_over_y + 250)

        self.game_over_group.add(game_over_sprite, self.highest_sprite, self.ok_sprite, self.reset_sprite)

        # 单词显示框
        input_rect_sprite = InputSprite(Game_Info.INPUT_BACKGROUND)
        self.input_rect_group = pygame.sprite.Group(input_rect_sprite)

        # 创建“游戏设置”图片
        self.game_set_sprite = GameSprite(Game_Info.GAME_SET_PINK)
        self.game_set_sprite.set_pos(Game_Info.SCREEN_RECT.width - self.game_set_sprite.rect.width - 10,
                                     Game_Info.SCREEN_RECT.height - self.game_set_sprite.rect.height - 10)
        self.game_set_sprite_group = pygame.sprite.Group(self.game_set_sprite)

        # 创建单词精灵组
        self.word_group = pygame.sprite.Group()
        self.__random_generate_word(Game_Info.GENERATE_WORD_NUM)

        text_sprite = ShowTextSprite("")
        self.text_group = pygame.sprite.Group(text_sprite)

        score_sprite = ScoreSprite("0")
        self.score_group = pygame.sprite.Group(score_sprite)

    def __update_sprite(self):
        """更新精灵"""
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.game_set_sprite_group.update()
        self.game_set_sprite_group.draw(self.screen)

        self.input_rect_group.update()
        self.input_rect_group.draw(self.screen)

        if not self.game_over_flag:
            self.word_group.update(self)
            self.word_group.draw(self.screen)

        self.text_group.update(self.word_content)
        self.text_group.draw(self.screen)

        self.score_group.update(str(self.total_score))
        self.score_group.draw(self.screen)

        # 更新游戏能量条
        if self.game_blood >= 0:
            self.__draw_game_blood()

        # 单词精灵拼写成功动画
        for bomb in self.bombs:
            if bomb.visible:
                bomb.draw()

    def start_game(self):
        """打字游戏开启"""
        while True:
            # 设置游戏刷新帧率
            self.game_clock.tick(Game_Info.FRAME_PRE_SEC)
            # 判断游戏结束
            if self.game_blood < 0 or self.game_over_flag:
                self.game_over_flag = True
            else:
                self.__bomb_action()
                self.__check_spell_word()
            self.__update_sprite()
            if self.game_over_flag:
                self.__game_over()
            self.__event_handle()
            pygame.display.update()

    def __event_handle(self):
        # 取出队列中的数据
        self.get_queue_data()

        # 遍历所有事件
        for event in pygame.event.get():
            try:
                if pygame.mixer.music.get_endevent() == Game_Info.MUSIC_END_EVENT and \
                        not pygame.mixer.music.get_busy():
                    # 如果music播放结束且没有音乐在播放就随机下一首
                    print("下一首")
                    random_music()
            except:
                pass
            if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                if not self.game_pause_flag:
                    pygame.quit()
                    sys.exit()
            elif event.type == Game_Info.CREATE_WORD_EVENT:  # 创建单词事件
                if not self.game_over_flag and not self.game_pause_flag:
                    # 游戏结束或者暂停就停止生成单词了
                    self.__random_generate_word(word_num=3)
            elif event.type == pygame.MOUSEMOTION:  # 鼠标移动事件
                x, y = event.pos  # 获取屏幕坐标位置
                if self.__is_on_set(x, y):
                    self.game_set_sprite.image = pygame.image.load(Game_Info.GAME_SET_BLUE)
                else:
                    self.game_set_sprite.image = pygame.image.load(Game_Info.GAME_SET_PINK)

                # 游戏结束鼠悬浮在确定按钮上变色
                if self.ok_sprite.rect.x <= x <= self.ok_sprite.rect.x + self.ok_sprite.rect.width and \
                        self.ok_sprite.rect.y <= y <= self.ok_sprite.rect.y + self.ok_sprite.rect.height:
                    self.ok_sprite.color = Game_Info.PINK
                else:
                    self.ok_sprite.color = Game_Info.BLUE

                # 游戏结束鼠标悬浮在重玩按钮上变色
                if self.reset_sprite.rect.x <= x <= self.reset_sprite.rect.x + self.reset_sprite.rect.width and \
                        self.reset_sprite.rect.y <= y <= self.reset_sprite.rect.y + self.reset_sprite.rect.height:
                    self.reset_sprite.color = Game_Info.PINK
                else:
                    self.reset_sprite.color = Game_Info.BLUE

            elif event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标点击事件
                x, y = event.pos  # 获取屏幕坐标位置

                # 点击游戏设置
                if self.__is_on_set(x, y):
                    # 判断游戏是否暂停
                    if not self.game_pause_flag:
                        self.__game_set()

                # 游戏结束鼠标点击确定按钮
                if self.ok_sprite.rect.x <= x <= self.ok_sprite.rect.x + self.ok_sprite.rect.width and \
                        self.ok_sprite.rect.y <= y <= self.ok_sprite.rect.y + self.ok_sprite.rect.height:
                    self.ok_sprite.color = Game_Info.PINK
                    pygame.quit()
                    sys.exit()

                # 游戏结束鼠标点击重玩按钮
                if self.reset_sprite.rect.x <= x <= self.reset_sprite.rect.x + self.reset_sprite.rect.width and \
                        self.reset_sprite.rect.y <= y <= self.reset_sprite.rect.y + self.reset_sprite.rect.height:
                    self.__reset_game()
            # 键盘事件
            elif event.type == pygame.KEYDOWN and not self.game_over_flag and not self.game_pause_flag:
                # 英文单引号的ASCII值是39、-是45、.是46
                # print(event.key)
                if (pygame.K_a <= event.key <= pygame.K_z) or event.key in (39, 45, 46):
                    if self.spell_ok:
                        # 如果单词拼写成功再按下键盘时清空内容
                        self.word_content = ""
                        self.spell_ok = False
                    # 控制单词长度
                    if len(self.word_content) < 40:
                        # 记录键盘输入的字符
                        self.word_content += pygame.key.name(event.key)
                    else:
                        print("Word to long")
                    self.__reset_word_sprite_color()
                    print(self.word_content)
                    # self.__delete_words()
                if event.key == pygame.K_BACKSPACE:
                    self.backspace_state = True
                    self.__delete_words()
            elif event.type == pygame.KEYUP:
                self.backspace_state = False
                self.backspace_count = 0
        # 实现长按backspace连续回删
        if self.backspace_state:
            self.backspace_count += 1
            if self.backspace_count > 30:
                self.__delete_words()

    def __game_set(self):
        """游戏设置"""
        print("游戏设置")
        self.game_pause_flag = True

        # 游戏暂停让单词下落速度变成0
        for word_sprite in self.word_group.sprites():
            word_sprite.speed = 0

        # 由于多进程不能共享全局变量，windows系统多进程不能传递模块对象
        # 所以把要用到的游戏配置封装起来
        game_info_dict = {
            "GAME_LEVEL": Game_Info.game_conf.game_level,
            "WORD_SIZE": Game_Info.WORD_SIZE,
            "INIT_BLOOD": Game_Info.INIT_BLOOD,
            "WORD_NORMAL_COLOR": Game_Info.WORD_NORMAL_COLOR,
            'SPELL_OK_COLOR': Game_Info.SPELL_OK_COLOR
        }
        p_game_set = multiprocessing.Process(target=start_game_set_win, args=(self.game_queue, game_info_dict))
        p_game_set.start()

    def __is_on_set(self, x, y):
        """
        检查是否在设置图片上
        :param x,y 鼠标的位置
        """
        img_set_x = self.game_set_sprite.rect.x
        img_set_y = self.game_set_sprite.rect.y
        img_set_w = self.game_set_sprite.rect.width
        img_set_h = self.game_set_sprite.rect.height

        if (img_set_x <= x <= img_set_x + img_set_w) and \
                (img_set_y <= y <= img_set_y + img_set_h):
            return True
        else:
            return False

    def __delete_words(self):
        """单词回删"""
        if self.word_content != "":
            self.word_content = self.word_content[:-1]
            print(self.word_content + "---" +
                  str(len(self.word_content)))
            if len(self.word_content) == 0:
                self.__reset_word_sprite_color()
            if self.spell_ok:
                # 如果单词拼写成功再按下键盘回删键时清空内容
                self.word_content = ""
                self.spell_ok = False

    def __reset_word_sprite_color(self):
        """重置单词精灵的颜色"""
        for word_sprite in self.word_group.sprites():
            word_sprite.color = pygame.color.Color(str(Game_Info.WORD_NORMAL_COLOR))

    def __random_generate_word(self, word_num=6):
        """
        随机生成单词精灵
        :param word_num:精灵数量
        :return:
        """
        count = 0
        while True:
            index = random.randint(0, len(self.words) - 1)
            eng_word = self.words[index]["eng_word"]
            cn_comment = self.words[index]["cn_comment"]
            # print(eng_word + "----" + cn_comment)
            word_sprite = WordSprite(eng_word, cn_comment)
            word_x = random.randint(
                0, Game_Info.SCREEN_RECT.width - word_sprite.rect.width)
            word_y = -random.randint(0, int(Game_Info.SCREEN_RECT.height / 10))
            word_sprite.rect.x = word_x
            word_sprite.rect.bottom = word_y
            word_sprite.speed = Game_Info.WORD_SPEED

            # 检查新单词精灵是否与单词精灵组中的精灵碰撞(重叠)
            words = pygame.sprite.spritecollide(word_sprite, self.word_group, False,
                                                pygame.sprite.collide_circle_ratio(1.3))
            # 碰撞(释放内存重新随机生成单词精灵)
            if len(words) > 0:
                word_sprite.kill()
                continue
            else:
                self.word_group.add(word_sprite)
                count += 1
            if count >= word_num:
                break

    def __game_over(self):
        highest_score = Game_Info.game_conf.game_highest_score
        if self.total_score > int(highest_score):
            highest_score = self.total_score
            Game_Info.game_conf.game_highest_score = highest_score
            Game_Info.game_conf.set_highest_score(highest_score)

        self.highest_sprite.display_text = u"历史最高分: %s" % highest_score
        self.highest_sprite.size = 50
        highest_sprite_x = (Game_Info.SCREEN_RECT.width - self.highest_sprite.rect.width) / 2
        self.highest_sprite.set_pos(highest_sprite_x, self.game_over_y + 150)
        self.game_over_group.update()
        self.game_over_group.draw(self.screen)

    def __check_spell_word(self):
        """检查拼写单词是否正确"""
        word_sprites = self.word_group.sprites()
        for word_sprite in word_sprites:
            if self.word_content.lower() in word_sprite.word_text.lower() \
                    and len(self.word_content) >= 1 \
                    and self.word_content[0].lower() == word_sprite.word_text[0].lower():

                # word_sprite.set_word_color(word_sprite.word_text, pygame.color.Color(Game_Info.SPELL_OK_COLOR))
                word_sprite.color = pygame.color.Color(Game_Info.SPELL_OK_COLOR)
                word_sprite.size = Game_Info.WORD_SIZE
                if self.word_content.lower() == word_sprite.word_text.lower():
                    self.game_blood += 1
                    self.total_score += 1
                    if self.game_blood >= 50:
                        self.game_blood = 50
                        print("满分加速")
                    else:
                        self.__draw_game_blood()
                    word_sprite.kill()
                    # 从预先创建完毕的爆炸中取出一个爆炸对象
                    for bomb in self.bombs:
                        if not bomb.visible:
                            # 爆炸对象设置爆炸位置
                            bomb.set_pos(word_sprite.rect.x,
                                         word_sprite.rect.y)
                            # 爆炸对象状态设置为True
                            bomb.visible = True
                            break
                    self.word_content = self.word_content + \
                                        "\t" + str(word_sprite.cn_comment)
                    self.spell_ok = True

    def __draw_game_blood(self, color=Game_Info.GREEN):
        """绘制游戏能量"""
        if self.game_blood <= 3:
            color = Game_Info.RED
        if self.game_blood >= 25:
            color = Game_Info.BLUE
        if self.game_blood >= 50:
            color = Game_Info.ORANGE
        # 绘制游戏能量
        pygame.draw.rect(self.screen, color,
                         pygame.Rect(Game_Info.GAME_BLOOD_RECT.x + 2, Game_Info.GAME_BLOOD_RECT.y,
                                     self.game_blood * 10, Game_Info.GAME_BLOOD_RECT.height))
        pygame.draw.rect(self.screen, Game_Info.WHITE,
                         Game_Info.GAME_BLOOD_RECT, 2)

    def __bomb_action(self):
        """开启爆炸动画"""
        for bomb in self.bombs:
            if bomb.visible:
                bomb.action()

    def __reset_game(self):
        """游戏重玩"""
        del self  # 释放内存
        pygame.quit()
        pygame.init()
        random_music()
        TypingGame().start_game()

    def get_queue_data(self):
        """获取队列的数据"""
        if not self.game_queue.empty():
            data = self.game_queue.get()
            result = data['result']
            save_type = data['type']
            print(result)
 
            if save_type not in 'quit':
                # 判断是临时保存还是，永久保存
                if save_type in 'permanent':
                    print(u"永久保存")
                    self.update_game_style(result)
                    # 修改配置文件
                    Game_Info.game_conf.set_game_level(result['game_level'])
                    Game_Info.game_conf.set_word_size(Game_Info.WORD_SIZE)
                    Game_Info.game_conf.set_game_init_blood(Game_Info.INIT_BLOOD)
                    Game_Info.game_conf.set_word_normal_color(Game_Info.WORD_NORMAL_COLOR)
                    Game_Info.game_conf.set_spell_ok_color(Game_Info.SPELL_OK_COLOR)
                elif save_type in 'temp_save':
                    print(u"临时保存")
                    self.update_game_style(result)
                
            self.game_pause_flag = False
            # 恢复单词下落速度
            for word_sprite in self.word_group.sprites():
                word_sprite.speed = Game_Info.WORD_SPEED

    def update_game_style(self, result):
        """更新游戏界面风格"""
        Game_Info.WORD_SPEED = Game_Info.GAME_LEVEL[str(result['game_level'])]
        Game_Info.game_conf.game_level = result['game_level']
        Game_Info.WORD_SIZE = int(result['word_size'])
        Game_Info.INIT_BLOOD = int(result['init_blood'])

        if result['normal_ccb']:
            Game_Info.WORD_NORMAL_COLOR = result['normal_ccb']
        if result['spell_ccb']:
            Game_Info.SPELL_OK_COLOR = result['spell_ccb']

        # 把游戏血条更新
        self.game_blood = Game_Info.INIT_BLOOD

        # 把当前显示的单词更新
        for word_sprite in self.word_group.sprites():
            word_sprite.size = Game_Info.WORD_SIZE
            word_sprite.speed = Game_Info.WORD_SPEED
            if result['normal_ccb']:
                word_sprite.color = pygame.color.Color(Game_Info.WORD_NORMAL_COLOR)


def main():
    random_music()
    TypingGame().start_game()
    # GameSetWin("游戏配置", None).start()


if __name__ == '__main__':
    main()
