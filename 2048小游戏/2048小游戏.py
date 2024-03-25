import pyglet

# 定义窗口宽高
win_height = 720
win_weight = 600
# 定义棋盘位置
start_x = 20
start_y = 100
# 定义棋盘格数
block = 6
# 棋盘总宽度与格子宽度
qipan_width = win_weight - 2 * start_x
block_width = qipan_width / block

lable_color = (119, 110, 101, 255)  # 文字颜色
bj_color = (250, 248, 239, 255)  # 背景颜色


# 主要代码
class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_init()

    def game_init(self):  # 字的绘制均在此处
        self.main_bath = pyglet.graphics.Batch()
        self.data = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        #         背景
        background_img = pyglet.image.SolidColorImagePattern(color=bj_color)
        self.background = pyglet.sprite.Sprite(background_img.create_image(win_weight, win_height), 0, 0)

        #         标题
        self.title_lable = pyglet.text.Label(text="2048小游戏", bold=True, color=lable_color, x=start_x,
                                             y=start_y + block_width + 30, font_size=36, batch=self.main_bath)

        #          成绩
        self.score = 0
        self.score_lable = pyglet.text.Label(text="成绩：%d" % self.score, bold=True, color=lable_color, x=200,
                                             y=start_y + block_width + 30, font_size=36, batch=self.main_bath)

        #         提示
        self.help_lable = pyglet.text.Label(text="使用上下左右键移动方块！", bold=True, color=lable_color, x=start_x,
                                            y=start_y - 30, font_size=15, batch=self.main_bath)

    def dow(self):
        self.clear()
        self.score_lable.text = "成绩：%d" % self.score
        self.background.draw()
        self.main_bath.draw()


# 创建窗口
win = Window(win_weight, win_height)
# 设置图标
ic = pyglet.image.load('图标/20250.jpg')
win.set_icon(ic)

pyglet.app.run()
