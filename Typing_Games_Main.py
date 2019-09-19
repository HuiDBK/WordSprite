# -*- Coding:UTF-8 -*-
"""
打字小游戏
Author:Mr Liu
Version:1.0
"""

import random
import pyautogui as gui
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
            english_words.append({"eng_word": words[0], "cn_comment": words[1]})
    return english_words


class TypingGame(object):
    """打字游戏主类"""

    # 用于标识单词拼写成功
    spell_ok = False

    def __init__(self):
        self.words = parser_words()
        self.screen = pygame.display.set_mode(Game_Info.SCREEN_RECT.size)
        self.game_clock = pygame.time.Clock()
        self.__create_sprite()
        self.score = [0]  # 把分数设置成数组方便把地址传递给单词精灵
        self.word_content = ""
        # 绘制游戏能量
        self.__draw_game_blood()
        # 设置创建单词的定时器
        pygame.time.set_timer(Game_Info.CREATE_WORD_EVENT, Game_Info.CREATE_WORD_INTERVAL)
        pygame.display.set_caption(Game_Info.GAME_NAME)
        pass

    def __create_sprite(self):
        """创建精灵和精灵组"""
        back_sprite = BackGroundSprite(Game_Info.GAME_BACKGROUND)
        input_rect_sprite = BackGroundSprite(Game_Info.WHITE_RECT_IMAGE)
        input_rect_sprite.rect.x = Game_Info.SCREEN_RECT.width / 2 - input_rect_sprite.rect.width / 2
        input_rect_sprite.rect.y = -30
        self.back_group = pygame.sprite.Group(back_sprite, input_rect_sprite)

        # 创建单词精灵组
        self.word_group = pygame.sprite.Group()
        self.__random_generate_word(Game_Info.GENERATE_WORD_NUM)

        text_sprite = ShowTextSprite("")
        self.text_group = pygame.sprite.Group(text_sprite)
        pass

    def __update_sprite(self):
        """更新精灵"""
        self.back_group.update()
        # 把背景精灵组中的所有精灵绘制到游戏屏幕上
        self.back_group.draw(self.screen)

        self.word_group.update(self.score)
        self.word_group.draw(self.screen)

        self.text_group.update(self.word_content)
        self.text_group.draw(self.screen)
        self.__draw_game_blood()
        pass

    def start_game(self):
        """打字游戏开启"""
        while True:
            # 判断游戏结束
            if self.score[0] < 0:
                self.__game_over()
            # 设置游戏刷新帧率
            self.game_clock.tick(Game_Info.FRAME_PRE_SEC)
            self.__event_handle()
            self.__check_spell_word()
            self.__update_sprite()
            pygame.display.update()

    def __event_handle(self):
        for event in pygame.event.get():  # 遍历所有事件
            if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                sys.exit()
            elif event.type == Game_Info.CREATE_WORD_EVENT:
                self.__random_generate_word(word_num=3)
            elif event.type == pygame.KEYDOWN:
                # 英文单引号的ASCII值是39
                if (pygame.K_a <= event.key <= pygame.K_z) or event.key == 39:
                    if self.spell_ok:
                        # 如果单词拼写成功再按下键盘时清空内容
                        self.word_content = ""
                        self.spell_ok = False
                    # 记录键盘输入的字符
                    self.word_content += pygame.key.name(event.key)
                    self.__reset_word_sprite_color()
                    print(self.word_content)
                elif event.key == pygame.K_BACKSPACE:
                    # 回删判断
                    if self.word_content != "":
                        self.word_content = self.word_content[:-1]
                        print(self.word_content + "---" + str(len(self.word_content)))
                        if len(self.word_content) == 0:
                            self.__reset_word_sprite_color()
                        if self.spell_ok:
                            # 如果单词拼写成功再按下键盘回删键时清空内容
                            self.word_content = ""
                            self.spell_ok = False

    def __reset_word_sprite_color(self):
        """重置单词精灵的颜色"""
        for word_sprite in self.word_group.sprites():
            word_sprite.set_word_color(word_sprite.word_text, Game_Info.GREEN_WORD)

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
            word_x = random.randint(0, Game_Info.SCREEN_RECT.width - word_sprite.rect.width)
            word_y = -random.randint(0, Game_Info.SCREEN_RECT.height / 10)
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

    @staticmethod
    def __game_over():
        result = gui.confirm("Game Over")
        pygame.quit()
        sys.exit()

    def __check_spell_word(self):
        """检查拼写单词是否正确"""
        word_sprites = self.word_group.sprites()
        for word_sprite in word_sprites:
            if self.word_content.lower() in word_sprite.word_text.lower() \
                    and len(self.word_content) >= 1 \
                    and self.word_content[0].lower() == word_sprite.word_text[0].lower():
                word_sprite.set_word_color(word_sprite.word_text, Game_Info.RED_WORD)
                if self.word_content.lower() == word_sprite.word_text.lower():
                    self.score[0] += 1
                    self.__draw_game_blood()
                    word_sprite.kill()
                    self.word_content = self.word_content + "\t" + str(word_sprite.cn_comment)
                    self.spell_ok = True
        pass

    def __draw_game_blood(self):
        """绘制游戏能量"""
        color = Game_Info.GREEN_WORD
        if self.score[0] <= 3:
            color = Game_Info.RED_WORD
        # 绘制游戏能量
        pygame.draw.rect(self.screen, color,
                         pygame.Rect(Game_Info.GAME_BLOOD_RECT.x + 2, Game_Info.GAME_BLOOD_RECT.y,
                                     self.score[0] * 10, Game_Info.GAME_BLOOD_RECT.height))
        pygame.draw.rect(self.screen, Game_Info.WHITE_WORD, Game_Info.GAME_BLOOD_RECT, 2)


if __name__ == '__main__':
    TypingGame().start_game()
