# -*- Coding:UTF-8 -*-
"""
打字小游戏
Author:Mr Liu
Version:1.0
"""

import random
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
    def __init__(self):
        self.words = parser_words()
        self.screen = pygame.display.set_mode(Game_Info.SCREEN_RECT.size)
        self.game_clock = pygame.time.Clock()
        self.__create_sprite()
        pygame.time.set_timer(Game_Info.CREATE_WORD_EVENT, Game_Info.CREATE_WORD_INTERVAL)
        pass

    def __create_sprite(self):
        """创建精灵和精灵组"""
        back_sprite = BackGroundSprite()
        self.back_group = pygame.sprite.Group(back_sprite)
        # 创建单词精灵组
        self.word_group = pygame.sprite.Group()
        self.__random_generate_word()
        pass

    def __update_sprite(self):
        """更新精灵"""
        self.back_group.update()
        # 把背景精灵组中的所有精灵绘制到游戏屏幕上
        self.back_group.draw(self.screen)

        self.word_group.update()
        self.word_group.draw(self.screen)
        pass

    def start_game(self):
        """打字游戏开启"""
        while True:
            # 设置游戏刷新帧率
            self.game_clock.tick(Game_Info.FRAME_PRE_SEC)
            self.__event_handle()
            # self.__check
            self.__update_sprite()
            pygame.display.update()

    def __event_handle(self):
        """事件监听"""
        for event in pygame.event.get():  # 遍历所有事件
            if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
                sys.exit()
            elif event.type == Game_Info.CREATE_WORD_EVENT:
                self.__random_generate_word()
            elif event.type == pygame.KEYDOWN:
                result = pygame.key.get_pressed()
                for i in range(len(result)):
                    if result[i] > 0:
                        key_value = pygame.key.name(i)
                        print(key_value)
                pass
        pass

    def __random_generate_word(self, word_num=6):
        """
        随机生成6个单词精灵
        :param word_num:
        :return:
        """
        count = 0
        while True:
            index = random.randint(0, len(self.words) - 1)
            eng_word = self.words[index]["eng_word"]
            cn_comment = self.words[index]["cn_comment"]
            print(eng_word + "----" + cn_comment)
            word_sprite = WordSprite(eng_word, cn_comment, 1)
            word_x = random.randint(0, Game_Info.SCREEN_RECT.width - word_sprite.rect.width)
            word_y = random.randint(0, Game_Info.SCREEN_RECT.height / 10)
            word_sprite.rect.x = word_x
            word_sprite.rect.bottom = word_y
            if count == 0:
                self.word_group.add(word_sprite)
                count += 1
            else:
                words = pygame.sprite.spritecollide(word_sprite, self.word_group, True)
                if len(words) > 0:
                    word_sprite.kill()
                    continue
                else:
                    self.word_group.add(word_sprite)
                    count += 1
            if count == word_num:
                break

    @staticmethod
    def __game_over():
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    typing_game = TypingGame()
    typing_game.start_game()