# -*- Coding:UTF-8 -*-
"""
打字小游戏
Author: Mr Liu
Version: 1.1
"""

import os
import sys
import random

import pyautogui as gui
from Game_Sprite import *

pygame.init()


def random_music():
    """随机播放音乐"""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(random.choice(Game_Info.GAME_MUSICS))
        pygame.mixer.music.play(loops=0)
    except Exception as e:
        print("无法加载音频设置，请检查电脑配置\t" + str(e))
        # 打印异常行数
        print("Line_Num:" + str(e.__traceback__.tb_lineno))


random_music()

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


class TypingGame(object):
    """打字游戏主类"""

    # 用于标识单词拼写成功
    spell_ok = False

    def __init__(self):
        self.words = parser_words()
        self.screen = pygame.display.set_mode(Game_Info.SCREEN_RECT.size)
        # 预先创建爆炸对象
        self.bombs = [Bomb(self) for _ in range(5)]
        self.game_clock = pygame.time.Clock()
        self.__create_sprite()
        self.total_score = 0  # 记录游戏拼写成功了多少个单词
        self.score = [5]     # 把分数设置成数组方便把地址传递给单词精灵
        self.word_content = ""
        self.backspace_state = False  # 键盘按下状态
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
        pass

    def __create_sprite(self):
        """创建精灵和精灵组"""

        # 背景精灵
        back_sprite = BackGroundSprite(Game_Info.GAME_BACKGROUND)
        self.back_group = pygame.sprite.Group(back_sprite)

        # 单词显示框
        input_rect_sprite = InputSprite(Game_Info.INPUT_BACKGROUND)
        self.input_rect_group = pygame.sprite.Group(input_rect_sprite)

        # 创建单词精灵组
        self.word_group = pygame.sprite.Group()
        self.__random_generate_word(Game_Info.GENERATE_WORD_NUM)

        text_sprite = ShowTextSprite("")
        self.text_group = pygame.sprite.Group(text_sprite)

        score_sprite = ScoreSprite("0")
        self.score_group = pygame.sprite.Group(score_sprite)
        pass

    def __update_sprite(self):
        """更新精灵"""
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.input_rect_group.update()
        self.input_rect_group.draw(self.screen)

        self.word_group.update(self)
        self.word_group.draw(self.screen)

        self.text_group.update(self.word_content)
        self.text_group.draw(self.screen)

        self.score_group.update(str(self.total_score))
        self.score_group.draw(self.screen)

        # 更新游戏能量条
        if self.score[0] >= 0:
            self.__draw_game_blood()

        # 单词精灵拼写成功动画
        for bomb in self.bombs:
            if bomb.visible:
                bomb.draw()

    def start_game(self):
        """打字游戏开启"""
        while True:
            # 判断游戏结束
            if self.score[0] < 0:
                self.__game_over()
            # 设置游戏刷新帧率
            self.game_clock.tick(Game_Info.FRAME_PRE_SEC)
            self.__bomb_action()
            self.__event_handle()
            self.__check_spell_word()
            self.__update_sprite()
            pygame.display.update()

    def __event_handle(self):
        for event in pygame.event.get():  # 遍历所有事件
            try:
                if pygame.mixer.music.get_endevent() == Game_Info.MUSIC_END_EVENT and not pygame.mixer.music.get_busy():
                    # 如果music播放结束且没有音乐在播放就随机下一首
                    print("下一首")
                    random_music()
            except Exception as e:
                pass
            if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                sys.exit()
            elif event.type == Game_Info.CREATE_WORD_EVENT:
                self.__random_generate_word(word_num=3)
            elif event.type == pygame.KEYDOWN:
                # 英文单引号的ASCII值是39  -是45
                if (pygame.K_a <= event.key <= pygame.K_z) or event.key == 39 or event.key == 45:
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
            word_sprite.set_word_color(word_sprite.word_text, Game_Info.BLUE)

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
        try:
            if not os.path.exists(Game_Info.SCORE_RECORD_FILE):
                # 只写模式打开文件，如果文件不存在会自动创建
                file = open(Game_Info.SCORE_RECORD_FILE, mode='w')
                file.close()
            # 读写模式打开
            score_file = open(Game_Info.SCORE_RECORD_FILE,
                              mode='r+', encoding='utf-8')
            # 读取出历史最高成绩
            lines = score_file.readline()
            if lines:
                highest_score = int(lines.split(":")[1])
                if self.total_score > highest_score:
                    # 首先先清空上次的最高纪录
                    score_file.seek(0)
                    score_file.truncate()
                    highest_score = self.total_score
                    score_file.write("HighestScore:" + str(self.total_score))
            else:
                highest_score = self.total_score
                score_file.write("HighestScore:" + str(self.total_score))
                score_file.close()
            result = gui.confirm("Game" + " " * 5 + "Over\n\n" + "Score:" + str(self.total_score) + "\n\n" +
                                 "HighestScore:" + str(highest_score),
                                 "Game Over", buttons=["退出", "重玩"])
        except Exception as file_e:
            print(file_e)
        if result == "退出":
            pygame.quit()
            sys.exit()
        elif result == "重玩":
            del self    # 释放内存
            pygame.quit()
            pygame.init()
            random_music()
            TypingGame().start_game()
        else:
            pygame.quit()
            sys.exit()

    def __check_spell_word(self):
        """检查拼写单词是否正确"""
        word_sprites = self.word_group.sprites()
        for word_sprite in word_sprites:
            if self.word_content.lower() in word_sprite.word_text.lower() \
                    and len(self.word_content) >= 1 \
                    and self.word_content[0].lower() == word_sprite.word_text[0].lower():
                word_sprite.set_word_color(
                    word_sprite.word_text, Game_Info.PINK)
                if self.word_content.lower() == word_sprite.word_text.lower():
                    self.score[0] += 1
                    self.total_score += 1
                    if self.score[0] >= 50:
                        self.score[0] = 50
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
        pass

    def __draw_game_blood(self, color=Game_Info.GREEN):
        """绘制游戏能量"""
        if self.score[0] <= 3:
            color = Game_Info.RED
        if self.score[0] >= 25:
            color = Game_Info.BLUE
        if self.score[0] >= 50:
            color = Game_Info.ORANGE
        # 绘制游戏能量
        pygame.draw.rect(self.screen, color,
                         pygame.Rect(Game_Info.GAME_BLOOD_RECT.x + 2, Game_Info.GAME_BLOOD_RECT.y,
                                     self.score[0] * 10, Game_Info.GAME_BLOOD_RECT.height))
        pygame.draw.rect(self.screen, Game_Info.WHITE,
                         Game_Info.GAME_BLOOD_RECT, 2)

    def __bomb_action(self):
        """开启爆炸动画"""
        for bomb in self.bombs:
            if bomb.visible:
                bomb.action()


if __name__ == '__main__':
    try:
        TypingGame().start_game()
    except Exception as e:
        print("未知异常\t" + str(e))
        print("Line_Num:" + str(e.__traceback__.tb_lineno))
