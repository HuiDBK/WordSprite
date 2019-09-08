# -*- Coding:UTF-8 -*-
"""
打字小游戏
Author:Mr Liu
Version:1.0
"""


def parser_words():
    """
    解析英语单词
    :return english_words
    """
    english_words = []
    word_contents = open("english_word.txt", encoding="gbk")
    for value in word_contents:
        print(value)


if __name__ == '__main__':
    parser_words()
    pass