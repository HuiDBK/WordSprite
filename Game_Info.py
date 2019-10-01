# -*- Coding:UTF-8 -*-
"""
游戏信息模块
Author: Mr Liu
Version: 1.1
"""
import tkinter
import pygame

GAME_NAME = "WordSprite"
SCREEN_RECT = pygame.Rect(0, 0, 1200, 800)
INPUT_RECT_WIDTH = 600
INPUT_RECT_HEIGHT = 100
GAME_BLOOD_RECT = pygame.Rect(SCREEN_RECT.width / 2 - 250, SCREEN_RECT.height - 26, 500, 25)

GAME_ICON = "image/rabbit.ico"
GAME_BACKGROUND = "image/game_bg.png"
INPUT_BACKGROUND = "image/input_bg.png"
SCORE_RECORD_FILE = "score_record.txt"

# 单词拼写成功后的消失动画
KILL_ANIMATION = ["image/000.png", "image/001.png", "image/002.png", "image/003.png", "image/004.png",
                  "image/005.png", "image/006.png", "image/007.png"]

FRAME_PRE_SEC = 60  # 游戏的刷新帧率
WORD_SIZE = 22      # 单词大小
WORD_SPEED = 0.5    # 单词下落速度

# 创建单词的时间间隔(毫秒)
CREATE_WORD_INTERVAL = 1000 * 4
# 首次生成单词的数量
GENERATE_WORD_NUM = 6

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


class GameOverDialog(object):
    """游戏结束对话框"""
    def __init__(self, main_game):
        self.main_game = main_game
        game_tk = tkinter.Tk()
        game_tk.title("Game Over")
        dialog_x = (game_tk.winfo_screenwidth() - 400) / 2
        dialog_y = (game_tk.winfo_screenheight() - 200) / 2
        dialog_size = "%dx%d+%d+%d" % (400, 200, dialog_x, dialog_y)
        game_tk.geometry(dialog_size)
        game_tk.resizable(0, 0)

        over_text = tkinter.Label(game_tk, text="Game    Over", font=("Arial", 15))
        over_text.pack(pady=20)

        btn_frame = tkinter.Frame(game_tk)
        exit_btn = tkinter.Button(btn_frame, text=u"退  出", command=self.exit_game)
        start_again_btn = tkinter.Button(btn_frame, text=u"重 玩", command=self.start_again)
        exit_btn.grid(row=0, column=0, padx=60, pady=50, ipadx=20)
        start_again_btn.grid(row=0, column=1, padx=60, ipadx=20)
        btn_frame.pack()
        # 进入消息循环

        game_tk.mainloop()

    def exit_game(self):
        print("exit game")

    def start_again(self):
        print("start again")


if __name__ == '__main__':
    GameOverDialog(None)
    pass
