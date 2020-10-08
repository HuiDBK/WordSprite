# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Hui
Description: {英文打字小游戏主入口模块}
"""
import os
import sys
import time
import traceback
import Game_View
from Game_View import *
from Game_Sprite import *


def center_pos():
    """设置游戏窗口相对电脑屏幕居中"""
    game_x = (Game_Info.SCREEN_X - Game_Info.SCREEN_RECT.width) / 2
    game_y = (Game_Info.SCREEN_Y - Game_Info.SCREEN_RECT.height) / 2
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (game_x, game_y)


def random_music():
    """随机播放背景音乐"""
    # 判断是否是静音模式
    print(Game_View.GameStartWin.voice_flag())
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(random.choice(Game_Info.GAME_MUSICS))
        pygame.mixer.music.play(loops=0)
    except Exception as e:
        print("无法加载音频，请检查电脑配置" + str(e))
        print(traceback.format_exc())

    if not Game_View.GameStartWin.voice_flag():
        pygame.mixer_music.set_volume(0)


def parser_words() -> dict:
    """
    解析英语单词
    :return {"eng_word": val, "cn_comment": val}
    """
    english_words = []
    word_contents = open(Game_Info.GAME_WORD_TEXT, encoding="gbk")
    for value in word_contents:
        value = value.lstrip()
        word_list = value.split(" ")
        words = [i for i in word_list if i != '']
        if len(words) >= 2:
            # 把解析好的单词和注释封装到字典中，然后加入列表
            english_words.append(
                {"eng_word": words[0], "cn_comment": words[1]})
    return english_words


class TypingGame(object):
    """打字游戏主类"""

    spell_ok = False            # 用于标识单词拼写成功
    game_pause_flag = False     # 游戏暂停标志
    game_over_flag = False      # 游戏结束标志
    game_quit_flag = False      # 游戏退出标志
    game_total_blood = Game_Info.GAME_BLOOD_RECT.width  # 游戏总能量(血条)

    # 游戏等级对照字典
    game_level_dict = {
        1: {"word_fall_speed": 0.3, "level_text": u"简单", "level_color": "green"},
        2: {"word_fall_speed": 0.5, "level_text": u"上手", "level_color": "blue"},
        3: {"word_fall_speed": 1.0, "level_text": u"中等", "level_color": "orange"},
        4: {"word_fall_speed": 1.5, "level_text": u"困难", "level_color": "red"},
        5: {"word_fall_speed": 2.0, "level_text": u"魔鬼", "level_color": "purple"}
    }

    @staticmethod
    def game_init():
        """游戏初始化"""
        # 初始化游戏字体
        pygame.font.init()

        # 设置游戏标题和图标
        pygame.display.set_caption(Game_Info.GAME_NAME)
        pygame.display.set_icon(pygame.image.load(Game_Info.GAME_ICON_32))

    @staticmethod
    def set_game_event():
        """设置游戏事件"""
        # 设置创建单词的定时器
        pygame.time.set_timer(Game_Info.CREATE_WORD_EVENT, Game_Info.CREATE_WORD_INTERVAL)

        # 设置游戏音乐结束事件
        try:
            pygame.mixer.music.set_endevent(Game_Info.MUSIC_END_EVENT)
        except Exception as e:
            print("无法设置音乐结束事件\t" + str(e))
            print(traceback.format_exc())

    def __init__(self):
        self.words = parser_words()
        self.game_conf = GameConfig()                   # 游戏配置信息
        self.game_default_voice = 20                    # 游戏默认音量
        self.use_time = 0                               # 记录游戏使用的时间
        self.total_score = 0                            # 记录游戏拼写成功了多少个单词
        self.word_content = ""                          # 键盘输入的单词
        self.backspace_count = 0                        # 回删键按下的次数

        # 预先创建动画对象
        self.animates = [Animation(self) for _ in range(5)]

        # 游戏初始血条值
        self.game_blood = int(self.game_conf.game_init_blood) * 10
        self.game_clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(Game_Info.SCREEN_RECT.size)

        self.game_init()
        self.set_game_event()       # 设置游戏事件
        self.__create_sprite()      # 创建游戏精灵

    def __create_sprite(self):
        """创建精灵和精灵组"""

        # 背景精灵
        back_sprite = ImageSprite(Game_Info.GAME_BACKGROUND)
        # 根据游戏屏幕的大小适配背景图(可能会导致背景图变形)
        back_sprite.transform_scale(
            back_sprite.image,
            (Game_Info.SCREEN_RECT.width, Game_Info.SCREEN_RECT.height)
        )
        self.back_group = pygame.sprite.Group(back_sprite)

        # 英文单词显示框
        input_rect_sprite = ImageSprite(Game_Info.INPUT_BACKGROUND)
        # 缩放图片
        input_rect_sprite.transform_scale(
            input_rect_sprite.image,
            (Game_Info.INPUT_RECT_WIDTH, Game_Info.INPUT_RECT_HEIGHT)
        )
        # 水平居中显示
        input_rect_sprite.hor_center(Game_Info.SCREEN_RECT)
        self.input_rect_group = pygame.sprite.Group(input_rect_sprite)

        # 创建“游戏设置”图片
        self.game_set_sprite = ImageSprite(Game_Info.GAME_SET_PINK)
        set_x = Game_Info.SCREEN_RECT.width - self.game_set_sprite.rect.width - 10
        set_y = Game_Info.SCREEN_RECT.height - self.game_set_sprite.rect.height - 10
        self.game_set_sprite.set_pos(set_x, set_y)
        self.game_set_sprite_group = pygame.sprite.Group(self.game_set_sprite)

        # 拼写的单词
        spell_word_sprite = SpellSprite(
            "",
            size=26,
            color=pygame.color.Color(self.game_conf.spell_ok_color)
        )
        spell_word_sprite.hor_center(Game_Info.SCREEN_RECT)
        spell_word_sprite.set_pos(spell_word_sprite.rect.x, 40)
        self.spell_word_group = pygame.sprite.Group(spell_word_sprite)

        # 创建单词精灵组
        self.word_group = pygame.sprite.Group()
        self.__random_generate_word(Game_Info.GENERATE_WORD_NUM)

        # 创建显示游戏时间精灵
        time_sprite = TextSprite(text="Time: 0", size=28, color=Game_Info.BLUE)
        time_sprite.set_pos(5, 0)
        self.time_group = pygame.sprite.Group(time_sprite)

        # 游戏分数
        self.score_sprite = TextSprite("Score: 0", size=30, color=Game_Info.BLUE)
        self.score_sprite.set_pos(Game_Info.SCREEN_RECT.width - self.score_sprite.rect.width - 20, 3)
        self.score_group = pygame.sprite.Group(self.score_sprite)

        # 游戏结束精灵(组)
        self.__game_over_sprite()

    def __game_over_sprite(self):
        """创建游戏结束的精灵(组)"""
        self.game_over_group = pygame.sprite.Group()

        game_over_sprite = TextSprite("Game  Over", 100, Game_Info.BLUE)
        game_over_sprite.rect.y = (Game_Info.SCREEN_RECT.height - game_over_sprite.rect.height - 400) / 2
        game_over_sprite.hor_center(Game_Info.SCREEN_RECT)

        game_level_text = self.game_level_dict[int(self.game_conf.game_level)]["level_text"]
        game_level_color = pygame.color.Color(self.game_level_dict[int(self.game_conf.game_level)]["level_color"])
        self.game_level_sprite = TextSprite(u"游戏等级: " + game_level_text, 50, game_level_color)
        self.game_level_sprite.rect.y = game_over_sprite.rect.y + 100 + 50
        self.game_level_sprite.hor_center(Game_Info.SCREEN_RECT)

        self.game_score_sprite = TextSprite(u"游戏分数: ", 50, Game_Info.BLUE)
        self.game_score_sprite.rect.y = game_over_sprite.rect.y + 200 + 50
        self.game_score_sprite.hor_center(Game_Info.SCREEN_RECT)

        self.highest_sprite = TextSprite(u"历史最高: ", 50, Game_Info.BLUE)
        self.highest_sprite.rect.y = game_over_sprite.rect.y + 300 + 50
        self.highest_sprite.hor_center(Game_Info.SCREEN_RECT)

        self.quit_sprite = TextSprite(u"退出", 50, Game_Info.BLUE)
        self.quit_sprite.set_pos(
            game_over_sprite.rect.x - self.quit_sprite.rect.width,
            game_over_sprite.rect.y + 400 + 10
        )

        self.reset_sprite = TextSprite(u"重 玩", 50, Game_Info.BLUE)
        self.reset_sprite.set_pos(
            game_over_sprite.rect.x + game_over_sprite.rect.width,
            game_over_sprite.rect.y + 400 + 10
        )

        self.game_over_group.add(
            game_over_sprite,
            self.game_level_sprite,
            self.game_score_sprite,
            self.highest_sprite,
            self.quit_sprite, self.reset_sprite
        )

    def __update_sprite(self):
        """更新精灵"""
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.game_set_sprite_group.update()
        self.game_set_sprite_group.draw(self.screen)

        self.input_rect_group.update()
        self.input_rect_group.draw(self.screen)

        # 计算游戏使用时间
        if not self.game_pause_flag and not self.game_over_flag:
            self.use_time += 0.1

        display_time = "Time: " + str(self.use_time / 6)
        self.time_group.update(display_time[:12])
        self.time_group.draw(self.screen)

        self.score_sprite.set_pos(Game_Info.SCREEN_RECT.width - self.score_sprite.rect.width - 20, 3)
        self.score_group.update("Score: " + str(self.total_score))
        self.score_group.draw(self.screen)

        # 判断是否游戏结束
        if self.game_over_flag:
            self.__game_over()
            game_level_text = self.game_level_dict[int(self.game_conf.game_level)]["level_text"]
            self.game_level_sprite.update("游戏等级: " + str(game_level_text))
            self.game_over_group.draw(self.screen)
        else:
            if not self.game_pause_flag:
                self.word_group.update(self)
            self.word_group.draw(self.screen)

            spell_ok_color = pygame.Color(self.game_conf.spell_ok_color)
            self.spell_word_group.update(self.word_content, spell_ok_color)
            self.spell_word_group.draw(self.screen)

            # 更新游戏能量条
            if 0 <= self.game_blood <= self.game_total_blood:
                self.__draw_game_blood()

        # 单词精灵拼写成功动画
        for animate in self.animates:
            if animate.visible:
                animate.draw()

    def start_game(self):
        """打字游戏开启"""
        # 随机播放背景音乐
        random_music()

        # 利用多线程完成游戏持续掉血
        drop_blood_t = threading.Thread(target=self.__drop_blood)
        drop_blood_t.start()

        while True:
            # 是否设置成静音
            if not Game_View.GameStartWin.voice_flag():
                pygame.mixer_music.set_volume(0)
            else:
                pygame.mixer_music.set_volume(self.game_default_voice)

            # 设置游戏刷新帧率
            self.game_clock.tick(Game_Info.FRAME_PRE_SEC)

            # 判断游戏结束
            if self.game_blood < 0:
                TypingGame.game_over_flag = True
            else:
                self.__animate_action()
                self.__check_spell_word()

            self.__update_sprite()
            self.__event_handle()
            pygame.display.update()

    def __event_handle(self):
        """游戏事件监听"""

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

            # 如果单击关闭窗口，则退出
            if event.type == pygame.QUIT and not self.game_pause_flag:
                pygame.quit()
                TypingGame.game_quit_flag = True
                sys.exit()

            # 创建单词事件
            elif event.type == Game_Info.CREATE_WORD_EVENT:
                if not self.game_over_flag and not self.game_pause_flag:
                    # 游戏结束或者暂停就停止生成单词了
                    self.__random_generate_word(word_num=3)

            # 鼠标移动事件
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos  # 获取屏幕坐标位置
                if self.__is_on_set(x, y):
                    self.game_set_sprite.image = pygame.image.load(Game_Info.GAME_SET_BLUE)
                else:
                    self.game_set_sprite.image = pygame.image.load(Game_Info.GAME_SET_PINK)

                # 游戏结束鼠标悬浮在确定按钮上变色
                if self.quit_sprite.rect.x <= x <= self.quit_sprite.rect.x + self.quit_sprite.rect.width and \
                        self.quit_sprite.rect.y <= y <= self.quit_sprite.rect.y + self.quit_sprite.rect.height:
                    self.quit_sprite.color = Game_Info.PINK
                    self.quit_sprite.update(self.quit_sprite.text)
                else:
                    self.quit_sprite.color = Game_Info.BLUE
                    self.quit_sprite.update(self.quit_sprite.text)

                # 游戏结束鼠标悬浮在重玩按钮上变色
                if self.reset_sprite.rect.x <= x <= self.reset_sprite.rect.x + self.reset_sprite.rect.width and \
                        self.reset_sprite.rect.y <= y <= self.reset_sprite.rect.y + self.reset_sprite.rect.height:
                    self.reset_sprite.color = Game_Info.PINK
                    self.reset_sprite.update(self.reset_sprite.text)
                else:
                    self.reset_sprite.color = Game_Info.BLUE
                    self.reset_sprite.update(self.reset_sprite.text)

            # 鼠标点击事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos  # 获取屏幕坐标位置

                # 点击游戏设置
                if self.__is_on_set(x, y):
                    # 判断游戏是否暂停
                    if not self.game_pause_flag:
                        TypingGame.game_pause_flag = True

                # 游戏结束鼠标点击退出按钮
                if self.quit_sprite.rect.x <= x <= self.quit_sprite.rect.x + self.quit_sprite.rect.width and \
                        self.quit_sprite.rect.y <= y <= self.quit_sprite.rect.y + self.quit_sprite.rect.height:
                    pygame.quit()
                    TypingGame.game_quit_flag = True
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
                    print(self.word_content)
                if event.key == pygame.K_BACKSPACE:
                    self.__delete_words()
            elif event.type == pygame.KEYUP:
                self.backspace_count = 0

        # 实现长按backspace连续回删
        # 使用键盘提供的方法获取键盘按键 - 按键元组
        keys_pressed = pygame.key.get_pressed()

        # 判断元组中对应的按键索引值 1
        if keys_pressed[pygame.K_BACKSPACE]:
            self.backspace_count += 1
            if self.backspace_count > 20:
                self.__delete_words()

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
            print(self.word_content + "---" + str(len(self.word_content)))
            if self.spell_ok:
                # 如果单词拼写成功再按下键盘回删键时清空内容
                self.word_content = ""
                self.spell_ok = False

    def __random_generate_word(self, word_num=5):
        """
        随机生成单词精灵
        :param word_num:精灵数量 默认5
        :return:
        """
        count = 0
        while len(self.word_group.sprites()) <= 30:
            index = random.randint(0, len(self.words) - 1)
            eng_word = self.words[index]["eng_word"]
            cn_comment = self.words[index]["cn_comment"]
            # print(eng_word + "----" + cn_comment)
            word_sprite = WordSprite(
                eng_word,
                cn_comment,
                speed=self.game_level_dict[int(self.game_conf.game_level)]['word_fall_speed'],
                size=int(self.game_conf.word_size),
                color=pygame.color.Color(str(self.game_conf.word_normal_color))
            )

            # 单词位置随机
            word_sprite.random_pos()

            # 检查新单词精灵是否与单词精灵组中的精灵碰撞(重叠)
            words = pygame.sprite.spritecollide(
                word_sprite, self.word_group, False,
                pygame.sprite.collide_circle_ratio(1)
            )

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
        """游戏结束"""
        self.game_score_sprite.hor_center(Game_Info.SCREEN_RECT)
        self.highest_sprite.hor_center(Game_Info.SCREEN_RECT)
        self.game_score_sprite.update(u"游戏分数: %s" % self.total_score)

        """
        history_score_dict
        {
            'level_0': "{'score': None,'use_time': None,'create_time': None}",
            'level_1': "{'score': None,'use_time': None,'create_time': None}",
            'level_2': "{...}",
            ...
        }
        """
        # 显示历史最高
        highest_score_str = self.game_conf.history_score_dict['level_' + str(int(self.game_conf.game_level))]
        highest_score_dict = eval(highest_score_str)
        highest_score = highest_score_dict['score']
        if highest_score is None or int(self.total_score) > int(highest_score):
            # 更新历史记录
            highest_score = self.total_score
            highest_score_dict['score'] = str(self.total_score)
            highest_score_dict['use_time'] = str(self.use_time)[:5] + 's'
            highest_score_dict['create_time'] = str(time.strftime("%Y-%m-%d %H:%M"))
            self.game_conf.set_highest_score(str(highest_score_dict), 'level_' + str(int(self.game_conf.game_level)))
        else:
            highest_score = highest_score_dict['score']

        self.highest_sprite.update(u"历史最高: %s" % highest_score)

    def __check_spell_word(self):
        """检查拼写单词是否正确"""
        word_sprites = self.word_group.sprites()
        for word_sprite in word_sprites:

            # 判断单词内容是否相同
            if self.word_content.lower() == word_sprite.text.lower():

                # 判断血条是否超过总血条数
                if self.game_blood < self.game_total_blood:
                    self.game_blood += 10

                self.total_score += 1
                self.spell_ok = True
                self.word_content = self.word_content + "\t" + str(word_sprite.cn_comment)
                word_sprite.kill()

                # 从预先创建完毕的动画中取出一个动画对象
                for animate in self.animates:
                    if not animate.visible:
                        # 设置动画位置
                        animate.set_pos(word_sprite.rect.x, word_sprite.rect.y)
                        # 动画对象状态设置为True
                        animate.visible = True
                        break

    def __draw_game_blood(self, color=Game_Info.GREEN):
        """绘制游戏能量"""

        if self.game_blood <= 3 * 10:
            color = Game_Info.RED
        if self.game_blood >= 25 * 10:
            color = Game_Info.BLUE
        if self.game_total_blood-30 <= self.game_blood <= self.game_total_blood:
            color = Game_Info.ORANGE

        # 绘制游戏能量
        pygame.draw.rect(
            self.screen, color,
            pygame.Rect(
                Game_Info.GAME_BLOOD_RECT.x + 2,
                Game_Info.GAME_BLOOD_RECT.y,
                self.game_blood,
                Game_Info.GAME_BLOOD_RECT.height
            )
        )
        pygame.draw.rect(self.screen, Game_Info.WHITE, Game_Info.GAME_BLOOD_RECT, 2)

    def __drop_blood(self):
        """持续掉血"""
        # if not self.game_pause_flag:
        #     if int(self.use_time) > 0 and (int(self.use_time) / 6) % 2 == 0:
        #         self.game_blood -= 0.5

        while not self.game_over_flag:
            if self.game_pause_flag:
                self.game_clock.tick(60)
            else:
                # 根据不同游戏等级掉血
                self.game_clock.tick(int(self.game_conf.game_level))
                self.game_blood -= 1

    def __animate_action(self):
        """开启单词拼写成功动画"""
        for animate in self.animates:
            if animate.visible:
                animate.action()

    def __reset_game(self):
        """游戏重玩"""
        del self  # 释放内存
        pygame.quit()
        pygame.init()
        random_music()
        TypingGame.game_over_flag = False
        TypingGame.game_quit_flag = False
        TypingGame().start_game()


def main():
    center_pos()
    # 启动游戏开始界面
    GameStartWin(title="Word Sprite").run()


if __name__ == '__main__':
    main()
