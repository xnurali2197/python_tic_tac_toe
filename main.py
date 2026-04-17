import sqlite3
import time
from functools import wraps
import datetime
import random

def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[DECORATOR] {func.__name__} — {end - start:.4f} soniya")
        return result
    return wrapper

class TicTacToe:
    def __init__(self, player_name="O'yinchi"):
        self._player_name = player_name
        self.board = [" " for _ in range(9)]
        self._create_db()

    @property
    def player_name(self):
        return self._player_name

    @player_name.setter
    def player_name(self, value):
        if len(value.strip()) < 2:
            raise ValueError("Ism kamida 2 harfdan iborat bo'lishi kerak!")
        self._player_name = value

    def _create_db(self):
        conn = sqlite3.connect("tictactoe.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY,
            player TEXT,
            result TEXT,
            date TEXT
        )''')
        conn.commit()
        conn.close()

    def print_board(self):
        print("\n")
        for i in range(3):
            print(f" {self.board[i*3]} | {self.board[i*3+1]} | {self.board[i*3+2]} ")
            if i < 2:
                print("---+---+---")

    def check_winner(self, mark):
        win_conditions = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        for condition in win_conditions:
            if all(self.board[i] == mark for i in condition):
                return True
        return False

    @timer_decorator
    def play_game(self):
        print(f"\n=== {self.player_name} vs Kompyuter (Tic-Tac-Toe) ===")
        self.board = [" " for _ in range(9)]
        current_player = "X"

        while True:
            self.print_board()
            if current_player == "X":
                try:
                    move = int(input(f"{self.player_name}, 1-9 orasidagi raqamni tanlang: ")) - 1
                    if move < 0 or move > 8 or self.board[move] != " ":
                        print("Noto'g'ri yoki band joy!")
                        continue
                except ValueError:
                    print("Raqam kiriting!")
                    continue
            else:
                # Kompyuter oddiy AI
                available = [i for i, spot in enumerate(self.board) if spot == " "]
                move = random.choice(available)

            self.board[move] = current_player

            if self.check_winner(current_player):
                self.print_board()
                if current_player == "X":
                    print(f"🎉 {self.player_name} g'alaba qozondi!")
                    result = "Win"
                else:
                    print("🤖 Kompyuter g'alaba qozondi!")
                    result = "Lose"
                self._save_score(result)
                break

            if " " not in self.board:
                self.print_board()
                print("Durrang!")
                self._save_score("Draw")
                break

            current_player = "O" if current_player == "X" else "X"

    def _save_score(self, result):
        conn = sqlite3.connect("tictactoe.db")
        cursor = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute("INSERT INTO scores (player, result, date) VALUES (?, ?, ?)",
                       (self.player_name, result, now))
        conn.commit()
        conn.close()

    @timer_decorator
    def show_scores(self):
        conn = sqlite3.connect("tictactoe.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scores ORDER BY id DESC LIMIT 10")
        scores = cursor.fetchall()
        conn.close()
        print(f"\n=== {self.player_name} ning O'yin Natijalari ===")
        for s in scores:
            print(f"{s[3]} | Natija: {s[2]}")

if __name__ == "__main__":
    game = TicTacToe()
    print("=== Tic-Tac-Toe O'yini ===")
    while True:
        print("\n1. O'yinni boshlash\n2. Natijalarni ko'rish\n3. O'yinchi nomini o'zgartirish\n4. Chiqish")
        choice = input("Tanlang (1-4): ").strip()
        if choice == "1":
            game.play_game()
        elif choice == "2":
            game.show_scores()
        elif choice == "3":
            new_name = input("Yangi ism: ").strip()
            try:
                game.player_name = new_name
            except ValueError as e:
                print(e)
        elif choice == "4":
            print("O'yin tugadi. Rahmat!")
            break
        else:
            print("Noto'g'ri tanlov!")
