"""
来源于蓝桥云课的教程：2048小游戏。用于提升自我编程能力与编程经验。
"""
# collections提供了一个字典的子类，其中defaultdict可以指定key值不存在时value的默认值
from collections import defaultdict
# random用来生成随机数
from random import randrange, choice
# curses用来在终端上显示图形界面。介于在windows上不支持curses库，所以使用其他GUI库替代，比如tkinter(标准库)\PyQt(第三方库)
from tkinter import *
from tkinter import messagebox


# 行矩阵转置
def transpose(field):
    return [list(row) for row in zip(*field)]


# 矩阵逆转。只是将矩阵的每一行倒序，而不是逆矩阵
def invert(field):
    return [row[:: -1] for row in field]


"""
2048游戏棋盘。默认4x4-2048
"""


class GameField(object):

    actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']  # 用户行为

    def __init__(self, height=4, width=4, win=2048):
        self.height = height  # 高
        self.width = width  # 宽

        self.win_value = win  # 过关分数
        self.score = 0  # 当前分数
        self.highscore = 0  # 最高分
        self.reset()  # 棋盘重置

    # 重置棋盘，在类进行实例化时自动调用，完成棋盘的重置，将棋盘的所有位置复位0，之后调用spawn函数，在随机位置生成游戏数值
    def reset(self):
        # 更新分数
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        # 初始化游戏开始界面
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        self.spawn()

    # 随机生成一个2或4
    def spawn(self):
        # 从100中随机取一个数，如果这个随机数大于89，new_element等于4，否则等于2
        new_element = 4 if randrange(100) > 89 else 2
        # 得到一个随机空白位置的元组坐标
        (x, y) = choice([(x, y) for x in range(self.width) for y in range(self.height) if self.field[x][y] == 0])
        self.field[x][y] = new_element

    # 一行向左合并
    def move_row_left(self, row):
        def tighten(row):
            """
            把零散的非零元素单元挤到一块
            :param row:每一行中的元素值
            :return: new_row 将非零元素拿出来后，使用0填充其余位置，形成完整个数的一行
            """
            # 先将非零的元素全拿出来加入到新列表
            new_row = [i for i in row if i != 0]
            # 按照原列表的长度，给新列表后面补零
            new_row += [0 for i in range(len(row) - len(new_row))]
            return new_row

        def merge(row):
            """
            对邻近元素进行合并
            :param row:每一行中的元素值
            :return:new_row 进行处理后的新一行
            """
            pair = False  # 控制每行是否可以进行合并
            new_row = []
            for i in range(len(row)):
                if pair:
                    # 合并后，加入乘以2后的元素在0 元素后面
                    new_row.append(2 * row[i])  # 乘以两倍的代码，即完成两个块的相加
                    # 更新分数
                    self.score += 2 * row[i]
                    pair = False
                else:
                    # 判断邻近元素能否合并
                    if i + 1 < len(row) and row[i] == row[i + 1]:
                        pair = True
                        # 可以合并时，新列表加入元素0
                        new_row.append(0)
                    else:
                        # 不能合并，新列表中加入该元素
                        new_row.append(row[i])
            assert len(new_row) == len(row)  # 断言：合并后不会改变行列大小，否则报错
            return new_row

        # 先挤到一块再合并再挤到一块
        return tighten(merge(tighten(row)))

    # 判断是否能够移动。实际上只判断能否向左移动，其他方向的移动，通过矩阵的转置与逆转之后的矩阵进行判断
    def move_is_possible(self, direction):
        """
        传入要移动的方向，判断能否在这个方向上移动
        :param direction: 需要移动的方向
        :return:
        """

        def row_is_left_moveable(row):
            """
            判断一行里面能否有元素进行左移或合并
            :param row: 一行的数据
            :return: Bool
            """

            def changes(i):
                # 当左边有空位（0），右边有数字时，可以向左移动
                if row[i] == 0 and row[i + 1] != 0:
                    return True
                # 当左边有一个数和右边的数相等时，可以向左合并
                if row[i] != 0 and row[i + 1] == row[i]:
                    return True
                return False

            return any(changes(j) for j in range(len(row) - 1))

        # 检查能否移动（合并也可以看作是在移动）
        check = dict()
        # 判断矩阵每一行有没有可以左移动的元素
        check['Left'] = lambda field: any(row_is_left_moveable(row=row) for row in field)
        # 判断矩阵每一行有没有可以右移的元素。这里只进行判断，所以矩阵变换之后不用再变换复原
        check['Right'] = lambda field: check['Left'](invert(field))
        check['Up'] = lambda field: check['Left'](transpose(field))
        check['Down'] = lambda field: check['Right'](transpose(field))
        # 如果direction是“上下左右”即字典check中存在的操作，那就执行对应的函数
        if direction in check:
            # 传入矩阵，执行对应函数
            return check[direction](self.field)
        else:
            return False

    # 棋盘操作：通过对矩阵进行转置与逆转，可以直接从左移得到其余三个方向的移动操作
    def move(self, direction):
        # 创建moves字典，把不同的棋盘操作作为不同的key，对应不同的方法函数
        moves = dict()
        moves['Left'] = lambda field: [self.move_row_left(row) for row in field]
        moves['Right'] = lambda field: invert(moves['Left'](invert(field)))
        moves['Up'] = lambda field: transpose(moves['Left'](transpose(field)))
        moves['Down'] = lambda field: transpose(moves['Right'](transpose(field)))
        # 判断棋盘操作是否存在且可行
        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False

    # 判断输赢
    def is_win(self):
        # 任意一个位置的数大于设定的win值时，游戏胜利
        return any(any(i >= self.win_value for i in row) for row in self.field)

    def is_gameover(self):
        # 无法移动和合并时，游戏失败
        return not any(self.move_is_possible(move) for move in self.actions)

    # 绘制游戏界面
    def draws(self, screen):
        """
        在设定的窗体中，绘制文字、边框线等对象
        :param screen: 绘制的窗体对象app
        :return:
        """
        help_string1 = 'W(向上) S(向下) A(向左) D(向右)'
        help_string2 = 'R(重置) Q(退出)'
        gameover_string = '游戏结束！'
        win_string = '恭喜！你赢了！'

        # 绘制函数
        def cast(string, screen, side="top", expand='no'):  # 将传入的内容展示到终端
            text_label = Label(screen, text=string + '\n', font=("FangSong", 12))
            text_label.pack(fill='x', padx=5, pady=2, anchor='center', side=side, expand=expand)

        # 绘制水平分割线的函数
        def draw_hor_separator():
            line = '+' + ('+---------' * self.width + '+')[1:]
            cast(line, screen[1])

        # 绘制竖直分割线的函数
        def drow_row(row):
            cast(''.join('|{: ^5}'.format(num) if num > 0 else '|     ' for num in row) + '|', screen[1])

        # 清空屏幕
        for wight in screen:
            for w in wight.winfo_children():
                w.destroy()
        # 绘制分数和最高分
        cast('分数:' + str(self.score), screen[0], side='left', expand='yes')
        # if not self.field:
        cast('最高分：' + str(self.highscore), screen[0], side='right', expand='yes')
        # 绘制行列边框分割线
        for row in self.field:
            draw_hor_separator()
            drow_row(row)
        draw_hor_separator()

        # 绘制提示文字
        if self.is_win():
            cast(win_string, screen[2])
        else:
            if self.is_gameover():
                cast(gameover_string, screen[2])
            else:
                cast(help_string1, screen[2])
        cast(help_string2, screen[2])


class Main(object):

    """
    用户行为：所有的有效输入都可以转换为“上下左右、游戏重置、退出”，用actions表示
    """
    actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']

    # ord() 函数以一个字符作为参数，返回参数对应的 ASCII 数值，便于和后面捕捉的键位关联
    # 电脑端或其他平台使用ASCII识别命令
    # letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']
    # 在手机端使用的键盘字母识别命令
    letter_codes = [ch for ch in 'WASDRQwasdrq']
    actions_dict = dict(zip(letter_codes, actions * 2))

    def __init__(self, *stdcr):
        self.game_field = GameField(win=2048)  # 实例化棋盘对象

        self.screen = stdcr

        # state存储当前状态，state_actions这个词典变量作为状态转换的规则，它的key是状态，value是返回下一个状态的函数。
        # self.state = 'Init'

        # 状态机
        self.state_actions = {
            'Init': self.inits,  # 初始化状态
            'Win': lambda: self.not_game('Win'),  # 胜利状态
            'Gameover': lambda: self.not_game('Gameover'),  # 失败状态
            'Game': self.game  # 游戏状态
            }
        self.screen[1].focus_set()
        self.inits()

    # inits函数初始化棋盘，使游戏变为初始状态
    def inits(self):

        """
        初始化游戏棋盘
        :return: Game
        """
        self.game_field.reset()
        self.state_actions['Game']()

    def game(self):
        # 根据状态画出游戏界面
        self.game_field.draws(self.screen)
        self.screen[1].bind('<Key>', self.keyworld)

    def keyworld(self, event):
        chars = event.char
        if chars not in self.actions_dict:
            # 电脑端识别方式
            # chars = event.keycode  # 键盘按下的键对应的ASCII
            # chars = event.char
            print('字典：', self.actions_dict.get(chars, ''))
            print('命令无效', chars)
        else:

            action = self.actions_dict[chars]
            if action == 'Restart':
                return self.state_actions['Init']()
            elif action == 'Exit':
                print('退出', action)
                messagebox.showinfo(title='彩蛋', message='您已退出游戏！')
                self.game_field.reset()
                # MyApp().destroy()
                return None
                # 这里如果游戏没有重置或退出，即使用了W\S\A\D等行为时，游戏移动一步。移动之后进行判断游戏是否结束。如果结束，则返回对应的状态：胜利或失败；没有结束就返回状态Game，表示还在游戏中。
            if self.game_field.move(action):
                print('移动成功', action)
                if self.game_field.is_win():
                    print('胜利！')
                    return self.state_actions['Win']()
                elif self.game_field.is_gameover():
                    print('gameover', self.game_field.is_gameover())
                    print('失败！')
                    return self.state_actions['Gameover']()
            else:
                print('移动失败', action)
        print('循环游戏命令输入：')
        return self.state_actions['Game']()

    def not_game(self, state):
        """
        展示游戏结束界面。读取用户输入得到的行为action，判断是重启游戏好还是结束游戏。
        :return: responses
        """
        self.state = state
        # 根据状态画出游戏界面
        self.game_field.draws(self.screen)
        # 读取用户输入得到的行为action，判断是重启游戏还是结束游戏
        self.screen[1].bind('<Key>', self.keyWorlds)

    def keyWorlds(self, event):
        chars = event.char
        if chars not in self.actions_dict:
            # 电脑端识别命令方式
            # chars = event.keycode  # 键盘按下的键ASCII
            # chars = event.char # 手机端识别方式
            print('命令无效', chars)
        else:
            action = self.actions_dict[chars]
            print('游戏出现结果，按键行为：', action)
            # defaultdict参数是callable类型，所以需要传一个函数（defaultdict生成一个特殊的字典，当字典中的key不存在时，我们可以取到key的值，其值就是我们自己设定的默认值
            responses = defaultdict(lambda: self.state)  # 设置默认值。当action为actions中的其他行为时（即用户输入了r\q以外的键），程序不会做出任何反应，以防止页面更改
            # 在字典中新建两个键值对
            responses['Restart'], responses['Exit'] = 'Init', 'Exit'  # Restart\Exit两种行为对应Init\Exit两种状态
            print('response保存的东西：', responses)
            if responses[action] == 'Restart':
                print('游戏重置')
                return self.state_actions['Init']()
            elif responses[action] == 'Exit':
                print('退出游戏！')
                messagebox.showinfo(title='彩蛋', message='您已退出游戏！')
                # MyApp().destroy()
                return None


class MyApp(Tk):
    """继承Tk，创建自己的桌面应用程序类"""

    def __init__(self):
        """构造函数"""

        super().__init__()

        self.title('2048小游戏')
        self.geometry('480x600')
        # ico_path = op.abspath("图标/xiaowu.ico")
        self.iconbitmap(default="图标/xiaowu.ico")

        self.frames1 = Frame(self, bg='#90c0c0', height=15)
        self.frames3 = Frame(self, bg='#90c0c0', height=10)
        self.frames2 = Frame(self, bg='#90c0c0', height=(600 - 2 * 25 - 50))

        self.frames1.pack(side='top', expand='No', fill='x', padx=5, pady=5)
        self.frames2.pack(side='top', expand='Yes', fill='x', padx=5, pady=5)
        self.frames3.pack(side='top', expand='No', fill='x', padx=5, pady=5)

        self.game()

    def game(self):
        Main(self.frames1, self.frames2, self.frames3)


if __name__ == '__main__':
    app = MyApp()
    app.mainloop()
