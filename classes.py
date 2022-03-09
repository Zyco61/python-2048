from gui2048 import *
from Data.database_handler import DataBaseHandler
import random
import datetime
database_handler = DataBaseHandler("madb.db")

class Partie(object):

    def __init__(self):
        self.scoreboard = Scoreboard()
        self.gui = GUI2048(4)
        self.grid = Grille()        
        
    def getGUI(self):
        return self.gui

    def isGameOver(self):
        for y in range(len(self.grid.grille)):
            for x in range(len(self.grid.grille)):
                if y - 1 >= 0:
                    if self.grid.grille[y][x] == self.grid.grille[y-1][x]:
                        return False
                if y + 1 <= len(self.grid.grille) - 1:
                    if self.grid.grille[y][x] == self.grid.grille[y+1][x]:
                        return False
                if x - 1 >= 0:
                    if self.grid.grille[y][x] == self.grid.grille[y][x-1]:
                        return False
                if x + 1 <= len(self.grid.grille) - 1:
                    if self.grid.grille[y][x] == self.grid.grille[y][x+1]:
                        return False
                if self.grid.grille[y][x] == 0:
                    return False
        return True

    def game(self):
        score = 0
        self.gui.refresh(self.grid.grille, score)

        self.grid.setup()
        self.gui.refresh(self.grid.grille, self.grid.score)

        while True:
            clic = self.gui.waitClick()
            if clic in ["R", "L", "U", "D"]:
                self.grid.deplacement(clic)
                self.gui.refresh(self.grid.grille, self.grid.score)
            if self.isGameOver():
                self.scoreboard.add_score(self.grid.score)
                print(self.scoreboard.scores())
                self.gui.gameOver()
          
class Grille(object):
    
    def __init__(self):
        self.grille = [[0 for i in range(4)] for j in range(4)]
        self.score = 0

    def setup(self):
        self.grille[random.randint(0, 3)][random.randint(0,3)] = 1
        while True:
            a = random.randint(0, 3)
            b = random.randint(0, 3)
            if not self.grille[a][b] == 0:
                continue
            self.grille[a][b] = 1
            break
        self.score = 4

    def deplacement(self, clic):
        if clic in ["R", "D"]:
            for y in range(len(self.grille)):
                for x in range(len(self.grille)):
                    if clic == "R":
                        if x + 1 <= 3 :
                            if self.grille[y][x] != 0:
                                if self.grille[y][x+1] == 0:
                                    self.grille[y][x+1] = self.grille[y][x]
                                    self.grille[y][x] = 0
                                elif self.grille[y][x+1] == self.grille[y][x]:
                                    self.score += ((self.grille[y][x]+1)**2)*2
                                    self.grille[y][x+1] += 1
                                    self.grille[y][x] = 0
                    elif clic == "D":
                        if y + 1 <= 3 :
                            if self.grille[y][x] != 0:
                                if self.grille[y+1][x] == 0:
                                    self.grille[y+1][x] = self.grille[y][x]
                                    self.grille[y][x] = 0
                                elif self.grille[y+1][x] == self.grille[y][x]:
                                    self.score += ((self.grille[y][x]+1)**2)*2
                                    self.grille[y+1][x] += 1
                                    self.grille[y][x] = 0
        elif clic in ["L", "U"]:
            for y in range(len(self.grille)-1, -1, -1):
                for x in range(len(self.grille)-1, -1, -1):
                    if clic == "L":
                        if x-1 >= 0 :
                            if self.grille[y][x] != 0:
                                if self.grille[y][x-1] == 0:
                                    self.grille[y][x-1] = self.grille[y][x]
                                    self.grille[y][x] = 0
                                elif self.grille[y][x-1] == self.grille[y][x]:
                                    self.score += ((self.grille[y][x]+1)**2)*2
                                    self.grille[y][x-1] += 1
                                    self.grille[y][x] = 0
                    elif clic == "U":
                        if y - 1 >= 0 :
                            if self.grille[y][x] != 0:
                                if self.grille[y-1][x] == 0:
                                    self.grille[y-1][x] = self.grille[y][x]
                                    self.grille[y][x] = 0
                                elif self.grille[y-1][x] == self.grille[y][x]:
                                    self.score += ((self.grille[y][x]+1)**2)*2
                                    self.grille[y-1][x] += 1
                                    self.grille[y][x] = 0

        while True:
            a = random.randint(0, 3)
            b = random.randint(0, 3)
            if self.grille[a][b] == 0:
                self.grille[a][b] = 1
                break

        
        

class Scoreboard(object):

    def __init__(self):
        id, username = self.username()
        self.id = id
        self.username = username

    def username(self):
        username = input("Quel est votre pseudo ? ")
        if not database_handler.user_exist(username):
            print('Création de votre compte, veuillez patienté !')
            id = database_handler.create_user(username)[0]
            print(f"Lancement du jeu ! Bonne chance {username} !")
        else:
            id, username = database_handler.get_user(username)
            print(f"Bon retour parmis nous {username} ! Bonne chance !")
        return id, username

    def scores(self):
        a = ""
        lb = database_handler.get_leaderboard()
        for i in range(len(lb)):
            a += f"#{i+1} : {lb[i][0]} => {lb[i][1]}\n"
        a = a[:-1]
        return a

    def add_score(self, score):
        database_handler.insert_score(score, self.id)

if __name__ == "__main__":
    p = Partie()
    p.game()