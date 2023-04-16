import os
import pandas as pd
import chess
import chess.svg
import pygame
import io

import pygame.image
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

        self.X = self.Y = 600
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.font_name = 'freesansbold.ttf'

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

        font = pygame.font.Font(self.font_name, 20)
        font_small = pygame.font.Font(self.font_name, 10)

        info = font_small.render('Press LEFT/RIGHT for moving within a game. '
                                 'Press UP/DOWN to change game', True, self.white, self.black)
        running = True
        update_board = False
        image = get_board_image(boards[j][i])
        while running:
            screen.fill(pygame.Color(self.black))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    update_board = True
                    if event.key == pygame.K_LEFT and i > 0:
                        i -= 1
                    if event.key == pygame.K_RIGHT and i < len(boards[j]) - 1:
                        i += 1
                    if event.key == pygame.K_DOWN and j > 0:
                        j -= 1
                        i = 0
                    if event.key == pygame.K_UP and j < len(boards) - 1:
                        j += 1
                        i = 0
                if event.type == pygame.QUIT:
                    running = False

            game_move = font.render(f'Game {j}, move {i}', True, self.white, self.black)
            who_is_white = 'our agent' if self.df.loc[j, 'agent_plays_white'] else 'test opponent'
            white_player = font.render(f'White: {who_is_white}', True, self.white, self.black)

            # For every move of the opponent, we display the top 5 moves of our agent
            if (who_is_white == 'our agent' and i % 2 == 1) or (who_is_white == 'test opponent' and i % 2 == 0):
                # top_moves = self.df.loc[j, 'top_moves']
                top_moves = "m1 - 1010,m2 - 1000,m3 - 800,m4 - 700,m5 - 550"
                top_moves = top_moves.split(',')
                screen.blit(font_small.render('Top 5 moves:', True, self.white, self.black), (self.X - 100, 10))
                # Could that be a loop?
                screen.blit(font_small.render(top_moves[0], True, self.white, self.black), (self.X - 100, 25))
                screen.blit(font_small.render(top_moves[1], True, self.white, self.black), (self.X - 100, 40))
                screen.blit(font_small.render(top_moves[2], True, self.white, self.black), (self.X - 100, 55))
                screen.blit(font_small.render(top_moves[3], True, self.white, self.black), (self.X - 100, 70))
                screen.blit(font_small.render(top_moves[4], True, self.white, self.black), (self.X - 100, 85))
            else:
                screen.blit(font_small.render('Top 5 moves:', True, self.white, self.black), (self.X - 100, 10))
                screen.blit(font_small.render('N/A', True, self.white, self.black), (self.X - 100, 25))

            screen.blit(game_move, (10, self.Y - 100))
            screen.blit(white_player, (10, self.Y - 100 + 25))
            screen.blit(info, (10, self.Y - 15))
            if update_board:
                image = get_board_image(boards[j][i])

            screen.blit(image, (0, 0))

            pygame.display.update()
            update_board = False

    @staticmethod
    def san_to_boards(san):
        moves = [x for x in san.split(' ') if '.' not in x]
        boards = []
        board = chess.Board()
        for move in moves:
            board.push_san(move)
            boards.append(board.copy())
        return boards
