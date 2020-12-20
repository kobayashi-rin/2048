#!/usr/bin/env python
# -*- coding: utf8 -*-
from game2048 import Game
import sys
import PySimpleGUI as sg

size = 4

game = Game()

game.put_tile()
game.put_tile()
layout = [[sg.Button(game.board[i][j], size=(4, 2), key=(i, j), pad=(0, 0)) for j in range(size)] for i in range(size)]

window = sg.Window('Minesweeper', layout)

while True:   # Event Loop
    event, values = window.read()
    if event in (None, '終了'):
        break

window.close()