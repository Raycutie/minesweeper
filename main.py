
import random
import time


class Mine:
    def explode(self):
        return "EXPLOSION"

    def __repr__(self):
        return 'M'


class Board:
    def __init__(self, height, width, mines):  # creates the board object
        self.__height = height
        self.__width = width
        self.__mines = mines
        self.values = {}
        self.screen = self.create_screen()

    def get_values(self):
        return self.values

    def get_mines(self):
        return self.__mines

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def mine_placement(self, starting_point):  # placerar ut minorna, kordinaterna för vissa rutor har en mina.
        list_of_invlaid_index = [starting_point]
        placed_mines = 0
        while placed_mines < self.get_mines():
            x = random.randint(1, self.get_height())
            y = random.randint(1, self.get_width())
            if [x, y] not in list_of_invlaid_index:
                self.values[str([x, y])] = Mine()
                list_of_invlaid_index.append([x, y])
                placed_mines += 1

    def surrounding_mines(self, row, column): #räknar ut hur många minor som ligger runt en ruta
        surrounding_mines = 0
        for x in range(row - 1, row + 2):
            for y in range(column - 1, column + 2):
                if 1 <= y <= self.get_width() and 1 <= x <= self.get_height():
                    if type(self.values.get(str([x, y]))) == Mine:
                        surrounding_mines += 1
        return surrounding_mines

    # Gör så att alla rutor på brädet har ett nr eller en mina som spelaren inte kan se
    def create_values_dict(self, starting_point):
        self.mine_placement(starting_point)
        for row in range(1, self.__height+1):
            for column in range(1, self.__width+1):
                if str([row, column]) not in self.values.keys():
                    self.values[str([row, column])] = self.surrounding_mines(row, column)

    def create_screen(self):  # creates the play board.at the player decided size.
        board = []
        for i in range(self.get_height()+1):
            board.append(["-" for j in range(self.get_width() + 1)])
        for m in range(self.get_width()+1):
            board[0][m] = str(m)
        for n in range(self.get_height()+1):
            board[n][0] = str(n)
        return board

    def update_screen(self, choosen_point): #uppdaterar brädet som spelaren ser
        x = choosen_point[0]
        y = choosen_point[1]
        try:
            if x==0 or y ==0:
                raise IndexError
            else:
                self.screen[x][y] = str(self.values.get(str(choosen_point)))

        except IndexError:
            print('Den kordinaten finns visst inte, försök igen')
            choosen_point = choose_point("Välj vilken koordinat du vill klargöra: ")
            return self.update_screen(choosen_point)
        else:
            if type(self.values.get(str(choosen_point))) == Mine:
                return Mine().explode()
            else:
                return True


class Player:
    def __init__(self, name, game_time=None, status=None):
        self.__name = name
        self.game_time = game_time
        self.status = status

    def set_status(self, a):
        self.status = a

    def get_name(self):
        return self.__name

    def get_game_time(self):
        return self.game_time

    def get_status(self):
        return self.status

    def set_game_time(self, a):
        self.game_time = a

    def __str__(self):
        return f"namn: {self.__name}, tid: {self.game_time}, status: {self.status}"


def person_name(): #funktion för personens namn.
    name = input('Vad heter du? ')
    name = name.strip(' ')
    if len(name) < 1:
        print('Du värkar inte ha skrivit in något')
        return person_name()
    else:
        return name

def menu():
    file = "status2.txt"
    choice = input("för att spela 1, för toplista 2: ")
    if choice == "1":
        try:
            name = person_name()
            player = Player(name)
            minesweeper(player)
        except RecursionError:
            print('Du har gjort för många fel inmatningar, starta om programmet.')
        else:
            add_new_player_to_highscore(player, file)
    elif choice == "2":
        stats(file)
    else:
        print("Inkorrekt inmatning, försök igen")
        menu()


def choose_point(uppmaning_i_input): # Takes 2 values as an input that correspont to a point on the board.
    try:
        x_value, y_value = input(uppmaning_i_input).split()
        x_value = int(x_value)
        y_value = int(y_value)
    except ValueError:
        print('Något gick fel, se exemplet på hur inskriften ska se ut och försök igen.')
        return choose_point(uppmaning_i_input)
    else:
        return [x_value, y_value]




def grid_size():
    uppmaning_i_input = "Välj storlek på brädet. (ex:4 4): "
    return choose_point(uppmaning_i_input)


def mine_nr(x, y):
    try:
        nr_of_mines = int(input("hur många minor ska vara en del av spelet? "))
        if nr_of_mines > x*y-1:
            raise ValueError('Antalet minor måste vara mindre än antalet rutor')
        elif nr_of_mines < 1:
            raise Exception('Antalet minor måste vare större än 0')
    except ValueError:
        print('Antalet minor måste vara mindre än antalet rutor, försök igen')
        return mine_nr(x, y)
    except Exception:
        print('Antalet minor måste vare större än 0, försök igen')
        return mine_nr(x, y)
    else:
        return nr_of_mines


def show_board(board):
    print('\n'.join(str(el) for el in board))

def minesweeper(player):
    input_list = grid_size()
    x = input_list[0]
    y = input_list[1]
    nr_of_mines = mine_nr(x, y)
    screen = Board(x, y, nr_of_mines) #skapar ett objekt av brädet
    show_board(screen.screen) #visar brädet i terminalen
    start_time = time.time()
    status = game_logic(screen)
    final_time = time.time()
    game_time = final_time - start_time
    player.set_game_time(game_time)
    player.set_status(status)
    print(player)


def game_logic(screen):
    list_of_moves = []
    starting_point = choose_point("Välj vilken koordinat du vill klargöra, ex: 1 1: ")
    list_of_moves.append(str(starting_point))
    screen.create_values_dict(starting_point) #skapar en dictoinary där varje kordinaten är nyckeln till
    #ett nummer eller en mina beroende på vad som är på motsvarande ruta.
    screen.update_screen(starting_point)
    condition = True
    while condition:
        if condition == "EXPLOSION":
            for i in screen.values.keys():
                if type(screen.values.get(i)) == Mine:
                    j = [int(i[1]), int(i[4])]
                    screen.update_screen(j)
            show_board(screen.screen)
            print("HA, förlorare")
            return "Förlorare"
        elif (screen.get_height()*screen.get_width()-len(list(set(list_of_moves)))) == screen.get_mines():
            show_board(screen.screen)
            print("Grattis, du är ingen förlorare")
            return "Vinnare"
        show_board(screen.screen)
        choosen_point = choose_point("Välj vilken koordinat du vill klargöra, ex: 1 1: ")
        condition = screen.update_screen(choosen_point)
        list_of_moves.append(str(choosen_point))


def file_handling_winners(FILE):
    players = []
    file = open(FILE, "r" , encoding = "utf-8")
    for line in file:
        line = line.split()
        a = Player(line[0], float(line[-1]), "Vinnare")
        players.append(a)
    file.close()
    return players


def stats(file):
    players = file_handling_winners(file)
    player_sort(players)
    N = 0
    for i in players:
        print(i)
        N += 1
        if N == 10:
            break


def player_sort(players):
    players.sort(key=lambda x: x.get_game_time())


def add_new_player_to_highscore(player, FILE):
    if player.get_status() == "Vinnare":
        file = open(FILE, "a", encoding="utf8")
        file.write(f"{player.get_name()} röjde alla minor på tiden: {player.get_game_time()}\n")
        file.close()
    elif player.get_status() == "Förlorare":
        pass


def main():
    menu()


if __name__ == "__main__":
    main()
