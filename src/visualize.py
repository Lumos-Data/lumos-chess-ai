import os
import pandas as pd
import chess
import chess.svg
import pygame
import io
from svglib.svglib import svg2rlg
import warnings

from config import Config

warnings.filterwarnings("ignore", message="x_order_2: colinear!")
warnings.filterwarnings("ignore", message="colinear!")


class Visualize:
    def __init__(self, config: Config, last=True):
        self.config_visual = config.visual

        self.output_dir = f'{config.root}/{self.config_visual["output_dir"]}'

        if not last:
            self.output_file = f'{self.output_dir}/{self.config_visual["exec_name"]}'
        else:
            files = [f for f in os.listdir(self.output_dir) if os.path.isfile(os.path.join(self.output_dir, f))]
            self.output_file = f'{self.output_dir}/{sorted(files)[-1]}'

        self.df = pd.read_csv(self.output_file)

        self.X = 500
        self.Y = 500

    def plot(self):
        pygame.init()
        screen = pygame.display.set_mode((self.X, self.Y))
        pygame.display.set_caption('Chess')

        def get_board_image(board):
            svg = chess.svg.board(board=board)
            f = open("temp/test.svg", "w")
            f.write(svg)
            f.close()
            drawing = svg2rlg('temp/test.svg')
            str_drawing = drawing.asString("png")
            byte_io = io.BytesIO(str_drawing)

            return pygame.image.load(byte_io)

        i, j = 0, 0
        boards = {j: self.san_to_boards(self.df.game.values[j]) for j in range(len(self.df))}
        font = pygame.font.Font('freesansbold.ttf', 20)

        font_small = pygame.font.Font('freesansbold.ttf', 10)
        info = font_small.render('Press LEFT/RIGHT for moving within a game. '
                    'Press UP/DOWN to change game', True, (255, 255, 255), (0, 0, 0))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        i -= 1
                    if event.key == pygame.K_RIGHT:
                        i += 1
                    if event.key == pygame.K_DOWN:
                        j -= 1
                        i = 0
                    if event.key == pygame.K_UP:
                        j += 1
                        i = 0
                if event.type == pygame.QUIT:
                    running = False

                image = get_board_image(boards[j][i])

                white, black = (255, 255, 255), (0, 0, 0)
                game_move = font.render(f'Game {j}, move {i}', True, white, black)
                who_is_white = 'our agent' if self.df.loc[j, 'agent_plays_white'] else 'test opponent'
                white_player = font.render(f'White: {who_is_white}', True, white, black)

                screen.blit(game_move, (10, self.Y - 100))
                screen.blit(white_player, (10, self.Y - 100 + 25))
                screen.blit(info, (10, self.Y - 15))
                screen.blit(image, (0, 0))

                pygame.display.update()

    @staticmethod
    def san_to_boards(san):
        moves = [x for x in san.split(' ') if '.' not in x]
        boards = []
        board = chess.Board()
        for move in moves:
            board.push_san(move)
            boards.append(board.copy())
        return boards
