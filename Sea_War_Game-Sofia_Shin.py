from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Ship:
    def __init__(self, start_dot, size, is_vertical=False):
        self.start_dot = start_dot
        self.size = size
        self.is_vertical = is_vertical
        self.lives=size

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.size):
            cur_x = self.start_dot.x-1
            cur_y = self.start_dot.y-1

            if self.is_vertical:
                cur_x += i
            else:
                cur_y += i
            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots


class Board:

    def __init__(self, is_user, hid=False, size=6):
        self.size = size
        self.hid = hid
        self.is_user=is_user

        self.count = 0

        self.field = [["O"] * size for _ in range(size)]

        self.busy = []
        self.ships = []
        self.shots = []


    def __str__(self):  # convert board to string
        if(self.is_user):
            print("User Board")
        else:
            print("Computer Board")
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    def isOutside(self, dot): #принимает точку и проверает outside or insdie the board
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size)) #returns true or false


    def add_ship(self, ship):

        for d in ship.dots:
            if self.isOutside(d) or d in self.busy:
              raise Exception(f"The cell {d.x+1, d.y+1} is busy or outside of the board. ")

        for dot in ship.dots:
            self.field[dot.x][dot.y] = "■"
            self.busy.append(dot)

        self.ships.append(ship)


        self.contour(ship)
 #contour 81 (put dots around the ship)

    def contour(self, ship, show=False): #show dots or not to show (False)
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.isOutside(cur)) and cur not in self.busy:
                    if show:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def shot(self, d):
        if self.isOutside(d):
            raise Exception("The shot is outside of the board")

        if d in self.shots:
            raise Exception("Shot in the same cell")

        self.shots.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, show=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "T"
        print("Мимо!")
        return False

def ask():
    while True:
        cords = input("Ваш ход: ").split()

        if len(cords) != 2:
            print(" Введите 2 координаты! ")
            continue

        x, y = cords

        if not (x.isdigit()) or not (y.isdigit()):
            print(" Введите числа! ")
            continue

        x, y = int(x), int(y)

        return Dot(x - 1, y - 1)


ship=Ship(start_dot= Dot(1,1),size=3,is_vertical=False)
ship2=Ship(start_dot= Dot(3,1),size=2,is_vertical=False)
ship3=Ship(start_dot= Dot(5,1),size=2,is_vertical=False)
ship4=Ship(start_dot= Dot(1,6),size=1,is_vertical=False)
ship5=Ship(start_dot= Dot(3,6),size=1,is_vertical=False)
ship6=Ship(start_dot= Dot(5,6),size=1,is_vertical=False)
ship7=Ship(start_dot= Dot(4,4),size=1,is_vertical=False)
user_board = Board(is_user=True,hid=False)

user_board.add_ship(ship)

user_board.add_ship(ship2)
user_board.add_ship(ship3)
user_board.add_ship(ship4)
user_board.add_ship(ship5)
user_board.add_ship(ship6)
user_board.add_ship(ship7)


computer_board=Board(False,hid=True)
computer_board.add_ship(ship)

computer_board.add_ship(ship2)
computer_board.add_ship(ship3)
computer_board.add_ship(ship4)
computer_board.add_ship(ship5)
computer_board.add_ship(ship6)
computer_board.add_ship(ship7)

num = 0
while True:
    print("-" * 20)
    print(user_board)
    print("-" * 20)
    print(computer_board)
    if num % 2 == 0: #четный  или не четный
        print("-" * 20)
        print("Ходит пользователь!")
        try:
            computer_board.shot(ask())
        except Exception as ex:
            print(ex.args)
            num -= 1

    else:
        print("-" * 20)
        print("Ходит компьютер!")
        try: #lets try the code and if there a code then it will catch this error/exception
            user_board.shot( Dot(randint(0, 5),randint(0, 5)) ) # randint - is a function from library random (imported at the top)
        except Exception as ex:
            print(ex.args)
            num -= 1 #

    print(f"Computer count:{computer_board.count}")
    print(f"User count:{user_board.count}")

    if computer_board.count == 7:
        print("-" * 20)
        print("Пользователь выиграл!")
        break

    if user_board.count == 7:
        print("-" * 20)
        print("Компьютер выиграл!")
        break
    num += 1