import flet as ft
import random
import os
import asyncio
 
class MemoryGame:
    def __init__(self, page):
        self.page = page
        self.setup_window()
        self.reset_game_data()
        self.highscore_files = {
            "Normal": "highscores_normal.txt",
            "Dificil": "highscores_dificil.txt"
        }
        self.card_images = [
            "strawberry.jpg",
            "pear.jpg",
            "orange.jpg",
            "lemon.jpg",
            "red apple.jpg",
            "kiwi.jpg",
            "green apple.jpg",
            "grapefruit.jpg",
            "Cartita1.png",
            "Cartita2.png",
            "Cartita3.png",
            "Cartita4.png",
            "back.jpg"
        ]
        self.initialize_highscore_files()
        self.show_welcome_screen()
 
    def setup_window(self):
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.bgcolor = ft.colors.BLACK
 
    def reset_game_data(self):
        self.difficulty = None
        self.cards = []
        self.selected_cards = []
        self.matched_pairs = set()
        self.flipped_cards = []
        self.username = None
        self.attempts = 0
        self.total_flips = 0
 
    def initialize_highscore_files(self):
        for file in self.highscore_files.values():
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    pass
 
    def create_cards(self):
        num_pairs = 8 if self.difficulty == "Normal" else 12
        card_values = list(range(num_pairs)) * 2
        random.shuffle(card_values)
        return card_values
 
    def show_welcome_screen(self):
        self.page.clean()
        self.page.title = "Memory Game"
 
        self.username_field = ft.TextField(
            label="Cual es tu nombre",
            width=300,
            autofocus=True,
            border_color=ft.colors.WHITE,
            color=ft.colors.WHITE,
            bgcolor=ft.colors.GREY_800
        )
 
        self.difficulty_dropdown = ft.Dropdown(
            label="Dificultad",
            options=[ft.dropdown.Option("Normal"), ft.dropdown.Option("Dificil")],
            width=300,
            bgcolor=ft.colors.GREY_800,
            color=ft.colors.WHITE,
            border_color=ft.colors.WHITE
        )
 
        welcome_content = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Memory game",
                            size=40,
                            color=ft.colors.WHITE,
                            weight=ft.FontWeight.BOLD),
                    ft.Divider(height=20, color=ft.colors.GREY_600),
                    self.username_field,
                    self.difficulty_dropdown,
                    ft.ElevatedButton(
                        "Comenzar",
                        on_click=self.start_game_from_button,
                        width=200,
                        height=50,
                        bgcolor=ft.colors.BLUE_700,
                        color=ft.colors.WHITE
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            width=600,
            padding=40,
            bgcolor=ft.colors.GREY_900,
            border_radius=15,
            border=ft.border.all(2, ft.colors.GREY_700),
            alignment=ft.alignment.center,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.colors.GREY_800, ft.colors.GREY_900]
            )
        )
 
        main_container = ft.Container(
            content=welcome_content,
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=ft.colors.BLACK
        )
 
        self.page.add(main_container)
        self.page.update()
 
    def start_game_from_button(self, e):
        username = self.username_field.value.strip()
        if not username:
            self.show_snackbar("Tienes que poner tu nombre")
            return
 
        if not self.difficulty_dropdown.value:
            self.show_snackbar("Tienes que seleccionar una dificultad")
            return
 
        self.difficulty = self.difficulty_dropdown.value
        self.username = username
        self.cards = self.create_cards()
        self.selected_cards = []
        self.matched_pairs = set()
        self.flipped_cards = []
        self.attempts = 0
        self.total_flips = 0
        self.update_ui()
 
    async def flip_card(self, e, index):
        if len(self.selected_cards) < 2 and index not in self.flipped_cards and index not in self.matched_pairs:
            self.selected_cards.append(index)
            self.flipped_cards.append(index)
            self.total_flips += 1
            self.update_ui()
 
            if len(self.selected_cards) == 2:
                self.attempts += 1
                await self.check_match()
 
    async def check_match(self):
        await asyncio.sleep(0.8)
 
        card1, card2 = self.selected_cards
        if self.cards[card1] == self.cards[card2]:
            self.matched_pairs.update([card1, card2])
            self.selected_cards.clear()
 
            if (self.difficulty == "Normal" and len(self.matched_pairs) == 16) or \
               (self.difficulty == "Dificil" and len(self.matched_pairs) == 24):
                await asyncio.sleep(0.5)
                self.show_winner()
        else:
            cards_to_flip = self.selected_cards.copy()
            self.selected_cards.clear()
            self.flipped_cards = [card for card in self.flipped_cards if card not in cards_to_flip]
            self.update_ui()
            await asyncio.sleep(0.15)
            self.update_ui()
 
    def update_ui(self):
        board_width = 700 if self.difficulty == "Normal" else 980
 
        game_container = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(f"Jugador: {self.username}",
                                    size=16,
                                    color=ft.colors.WHITE),
                            ft.Text(f"Intentos: {self.attempts}",
                                    size=16,
                                    color=ft.colors.WHITE),
                            ft.Text(f"Pares: {len(self.matched_pairs)//2}/" +
                                    ("8" if self.difficulty == "Normal" else "12"),
                                    size=16,
                                    color=ft.colors.WHITE),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        width=board_width - 50
                    ),
                    ft.Container(
                        content=self.create_game_board(),
                        alignment=ft.alignment.center
                    )
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            width=board_width,
            padding=20,
            bgcolor=ft.colors.BLACK,
            border_radius=10
        )
 
        self.page.clean()
        self.page.add(
            ft.Container(
                content=game_container,
                alignment=ft.alignment.center,
                expand=True,
                bgcolor=ft.colors.BLACK
            )
        )
        self.page.update()
 
    def create_game_board(self):
        grid = ft.Column(spacing=10, alignment=ft.MainAxisAlignment.CENTER)
        if self.difficulty == "Normal":
            rows, cols = 4, 4
        else:
            rows, cols = 4, 6
        for row in range(rows):
            row_controls = []
            for col in range(cols):
                index = row * cols + col
                if index >= len(self.cards):
                    continue
                is_matched = index in self.matched_pairs
                is_flipped = index in self.flipped_cards or is_matched
 
                card = ft.Container(
                    content=ft.Image(
                        src=self.card_images[self.cards[index]] if is_flipped else self.card_images[12],
                        width=120,
                        height=120
                    ),
                    on_click=None if is_matched else (lambda e, idx=index: self.page.run_task(self.flip_card, e, idx)),
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.BLACK,
                    border_radius=10,
                    width=140,
                    height=140,
                    padding=10,
                    border=ft.border.all(
                        2,
                        ft.colors.BLUE if index in self.selected_cards else ft.colors.GREY_700
                    )
                )
                row_controls.append(card)
 
            grid.controls.append(ft.Row(row_controls, spacing=10, alignment=ft.MainAxisAlignment.CENTER))
 
        return ft.Container(content=grid, padding=20)
 
    def show_winner(self):
        score = self.attempts
        if self.username and self.difficulty:
            self.save_highscore(self.username, score)
 
        highscores = self.load_highscores()
 
        leaderboard = ft.Column(
            [ft.Text(f"Mejores 5 jugadores - Modo {self.difficulty}", size=24, color=ft.colors.WHITE)],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )
 
        if not highscores:
            leaderboard.controls.append(ft.Text("Todavia no Hay puntuajes", color=ft.colors.WHITE70))
        else:
            for i, (name, scr) in enumerate(highscores[:5], start=1):
                leaderboard.controls.append(
                    ft.Text(f"{i}. {name}: {scr} intentos",
                            color=ft.colors.BLUE_300 if name == self.username else ft.colors.WHITE)
                )
 
        winner_content = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Ganaste",
                            size=30,
                            color=ft.colors.GREEN,
                            weight=ft.FontWeight.BOLD),
                    ft.Text(f"Te tomo {score} intentos",
                            size=20,
                            color=ft.colors.WHITE),
                    ft.Divider(height=20, color=ft.colors.GREY_600),
                    leaderboard,
                    ft.ElevatedButton(
                        "Jugar otra vez",
                        on_click=self.reset_game,
                        width=200,
                        bgcolor=ft.colors.BLUE_700,
                        color=ft.colors.WHITE
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            width=600,
            padding=40,
            bgcolor=ft.colors.GREY_900,
            border_radius=15,
            border=ft.border.all(2, ft.colors.GREY_700),
            alignment=ft.alignment.center,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.colors.GREY_800, ft.colors.GREY_900]
            )
        )
   
        self.page.clean()
        self.page.add(winner_content)
        self.page.update()
 
    def save_highscore(self, username, score):
        try:
            with open(self.highscore_files[self.difficulty], "a") as file:
                file.write(f"{username}:{score}\n")
        except Exception as e:
            self.show_snackbar(f"Error: {str(e)}")
 
    def load_highscores(self):
        try:
            file = self.highscore_files[self.difficulty]
            if not os.path.exists(file):
                return []
 
            highscores = []
            with open(file, "r") as file:
                for line in file.readlines():
                    if ":" in line:
                        name, score = line.strip().split(":")
                        highscores.append((name, int(score)))
            return sorted(highscores, key=lambda x: x[1])[:5]
        except Exception as e:
            self.show_snackbar(f"Error: {str(e)}")
            return []
 
    def reset_game(self, e=None):
        self.reset_game_data()
        self.show_welcome_screen()
 
    def show_snackbar(self, message, duration=2000):
        self.page.snack_bar = ft.SnackBar(
            ft.Text(message),
            duration=duration,
            bgcolor=ft.colors.BLUE
        )
        self.page.snack_bar.open = True
        self.page.update()
 
def main(page: ft.Page):
    game = MemoryGame(page)
 
ft.app(target=main, assets_dir="assets")